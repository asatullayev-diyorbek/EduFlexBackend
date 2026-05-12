from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Assignment, AssignmentTask, Submission, TaskResponse
from .serializers import (
    AssignmentListSerializer, AssignmentDetailSerializer,
    AssignmentCreateSerializer, SubmissionSerializer, SubmissionListSerializer,
)
from .grading import grade_submission


def is_teacher(user):
    return user.role in ('teacher', 'admin')


# ── Assignment CRUD ───────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def assignment_list(request):
    if request.method == 'GET':
        if is_teacher(request.user):
            qs = Assignment.objects.filter(teacher=request.user)
        else:
            qs = Assignment.objects.filter(is_published=True)
        return Response(AssignmentListSerializer(qs, many=True).data)

    if not is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)

    serializer = AssignmentCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(teacher=request.user)
    return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def assignment_detail(request, pk):
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    if request.method == 'GET':
        if not is_teacher(request.user) and not assignment.is_published:
            return Response({'detail': "Ruxsat yo'q"}, status=403)
        return Response(AssignmentDetailSerializer(assignment).data)

    if not is_teacher(request.user) or assignment.teacher != request.user:
        return Response({'detail': "Ruxsat yo'q"}, status=403)

    if request.method == 'DELETE':
        assignment.delete()
        return Response(status=204)

    serializer = AssignmentCreateSerializer(assignment, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_assignment(request, pk):
    if not is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)
    try:
        assignment = Assignment.objects.get(pk=pk, teacher=request.user)
    except Assignment.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    assignment.is_published = not assignment.is_published
    assignment.save(update_fields=['is_published'])
    return Response({'is_published': assignment.is_published})


# ── Student: start / save / submit ───────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_submission(request, pk):
    if is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)
    try:
        assignment = Assignment.objects.get(pk=pk, is_published=True)
    except Assignment.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    submission, _ = Submission.objects.get_or_create(
        student=request.user, assignment=assignment,
        defaults={'status': 'draft'},
    )
    if submission.status == 'graded':
        return Response({'detail': 'Topshiriq allaqachon baholangan'}, status=400)

    return Response(SubmissionSerializer(submission).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_responses(request, pk):
    try:
        submission = Submission.objects.get(student=request.user, assignment_id=pk)
    except Submission.DoesNotExist:
        return Response({'detail': 'Avval topshiriqni boshlang'}, status=400)

    if submission.status == 'submitted':
        return Response({'detail': 'Topshiriq allaqachon yuborilgan'}, status=400)

    for item in request.data.get('responses', []):
        task_id = item.get('task_id')
        text    = item.get('response_text', '')
        try:
            task = AssignmentTask.objects.get(pk=task_id, assignment=submission.assignment)
        except AssignmentTask.DoesNotExist:
            continue
        TaskResponse.objects.update_or_create(
            submission=submission, task=task,
            defaults={'response_text': text},
        )
    return Response({'saved': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assignment(request, pk):
    try:
        submission = Submission.objects.get(student=request.user, assignment_id=pk)
    except Submission.DoesNotExist:
        return Response({'detail': 'Avval topshiriqni boshlang'}, status=400)

    if submission.status in ('submitted', 'graded'):
        return Response({'detail': 'Allaqachon yuborilgan'}, status=400)

    for item in request.data.get('responses', []):
        task_id = item.get('task_id')
        text    = item.get('response_text', '')
        try:
            task = AssignmentTask.objects.get(pk=task_id, assignment=submission.assignment)
        except AssignmentTask.DoesNotExist:
            continue
        TaskResponse.objects.update_or_create(
            submission=submission, task=task,
            defaults={'response_text': text},
        )

    grade_submission(submission)
    submission.status       = 'submitted'
    submission.submitted_at = timezone.now()
    submission.save(update_fields=['status', 'submitted_at'])

    return Response(SubmissionSerializer(submission).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_submission(request, pk):
    try:
        submission = Submission.objects.get(student=request.user, assignment_id=pk)
    except Submission.DoesNotExist:
        return Response(None)
    return Response(SubmissionSerializer(submission).data)


# ── Teacher: view & grade submissions ────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_list(request, pk):
    if not is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)
    try:
        assignment = Assignment.objects.get(pk=pk, teacher=request.user)
    except Assignment.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    qs = Submission.objects.filter(assignment=assignment).exclude(status='draft')
    return Response(SubmissionListSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_detail(request, sub_id):
    if not is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)
    try:
        submission = Submission.objects.get(pk=sub_id)
    except Submission.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    if submission.assignment.teacher != request.user:
        return Response({'detail': "Ruxsat yo'q"}, status=403)

    return Response(SubmissionSerializer(submission).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def grade_submission_view(request, sub_id):
    if not is_teacher(request.user):
        return Response({'detail': "Ruxsat yo'q"}, status=403)
    try:
        submission = Submission.objects.get(pk=sub_id)
    except Submission.DoesNotExist:
        return Response({'detail': 'Topilmadi'}, status=404)

    if submission.assignment.teacher != request.user:
        return Response({'detail': "Ruxsat yo'q"}, status=403)

    total = 0.0
    for item in request.data.get('task_scores', []):
        try:
            resp = TaskResponse.objects.get(pk=item['response_id'], submission=submission)
            resp.score           = float(item.get('score', 0))
            resp.grader_feedback = item.get('feedback', '')
            resp.auto_graded     = False
            resp.save()
            total += resp.score
        except (TaskResponse.DoesNotExist, KeyError, ValueError):
            continue

    submission.score    = total
    submission.feedback = request.data.get('feedback', '')
    submission.status   = 'graded'
    submission.save(update_fields=['score', 'feedback', 'status'])

    return Response(SubmissionSerializer(submission).data)
