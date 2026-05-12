from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone

from .models import Test, Question, Attempt, Answer
from .serializers import (
    TestSerializer, QuestionSerializer,
    AttemptSerializer, AttemptListSerializer, AnswerSerializer,
)
from .grading import grade_answer


# ── Tests ──────────────────────────────────────────────────────────────────


@api_view(['GET', 'POST'])
def test_list(request):
    if request.method == 'GET':
        user = request.user
        if user.role == 'student':
            qs = Test.objects.filter(is_active=True)
        elif user.role == 'teacher':
            qs = Test.objects.filter(created_by=user)
        else:
            qs = Test.objects.all()
        qs = qs.order_by('-created_at')
        return Response(TestSerializer(qs, many=True).data)

    # POST — teacher/admin only
    if request.user.role not in ('teacher', 'admin'):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TestSerializer(data=request.data)
    if serializer.is_valid():
        test = serializer.save(created_by=request.user)
        return Response(TestSerializer(test).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def test_detail(request, pk):
    try:
        test = Test.objects.get(pk=pk)
    except Test.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TestSerializer(test).data)

    # Write operations — owner or admin
    if request.user.role not in ('admin',) and test.created_by != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = TestSerializer(test, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(TestSerializer(test).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Questions ──────────────────────────────────────────────────────────────


@api_view(['GET', 'POST'])
def question_list(request, test_pk):
    try:
        test = Test.objects.get(pk=test_pk)
    except Test.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        qs = test.questions.all()
        return Response(QuestionSerializer(qs, many=True).data)

    if request.user.role not in ('admin',) and test.created_by != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    data = {**request.data, 'test': test.pk}
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save(test=test)
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.select_related('test').get(pk=pk)
    except Question.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(QuestionSerializer(question).data)

    test = question.test
    if request.user.role not in ('admin',) and test.created_by != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = QuestionSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(QuestionSerializer(question).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Attempts ───────────────────────────────────────────────────────────────


@api_view(['GET', 'POST'])
def attempt_list(request):
    if request.method == 'GET':
        user = request.user
        if user.role == 'student':
            qs = Attempt.objects.filter(user=user).order_by('-started_at')
        elif user.role == 'teacher':
            qs = Attempt.objects.filter(test__created_by=user).order_by('-started_at')
        else:
            qs = Attempt.objects.all().order_by('-started_at')
        return Response(AttemptListSerializer(qs, many=True).data)

    # POST — start new attempt
    test_id = request.data.get('test_id')
    if not test_id:
        return Response({'detail': 'test_id required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        test = Test.objects.get(pk=test_id, is_active=True)
    except Test.DoesNotExist:
        return Response({'detail': 'Test not found or inactive'}, status=status.HTTP_404_NOT_FOUND)

    attempt = Attempt.objects.create(user=request.user, test=test)
    return Response(AttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def attempt_detail(request, pk):
    try:
        attempt = Attempt.objects.prefetch_related('answers').get(pk=pk)
    except Attempt.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role == 'student' and attempt.user != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    return Response(AttemptSerializer(attempt).data)


@api_view(['POST'])
def submit_answer(request, attempt_pk):
    try:
        attempt = Attempt.objects.get(pk=attempt_pk, status='in_progress')
    except Attempt.DoesNotExist:
        return Response({'detail': 'Attempt not found or already finished'}, status=status.HTTP_404_NOT_FOUND)

    if attempt.user != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    question_id = request.data.get('question_id')
    user_answer = request.data.get('answer')

    try:
        question = Question.objects.get(pk=question_id, test=attempt.test)
    except Question.DoesNotExist:
        return Response({'detail': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    is_correct, points_earned = grade_answer(question, user_answer)

    answer, _ = Answer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            'user_answer': user_answer,
            'is_correct': is_correct,
            'points_earned': points_earned,
        }
    )
    return Response(AnswerSerializer(answer).data)


@api_view(['POST'])
def finish_attempt(request, pk):
    try:
        attempt = Attempt.objects.prefetch_related('answers__question').get(pk=pk, status='in_progress')
    except Attempt.DoesNotExist:
        return Response({'detail': 'Attempt not found or already finished'}, status=status.HTTP_404_NOT_FOUND)

    if attempt.user != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    time_spent = request.data.get('time_spent')

    total_score = sum(a.points_earned for a in attempt.answers.all())
    max_score = sum(q.points for q in attempt.test.questions.all())
    percentage = round((total_score / max_score * 100) if max_score > 0 else 0, 1)

    attempt.score = total_score
    attempt.max_score = max_score
    attempt.percentage = percentage
    attempt.status = 'completed'
    attempt.finished_at = timezone.now()
    if time_spent is not None:
        attempt.time_spent = int(time_spent)
    attempt.save()

    return Response(AttemptSerializer(attempt).data)


@api_view(['GET'])
def test_attempts(request, test_pk):
    try:
        test = Test.objects.get(pk=test_pk)
    except Test.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in ('admin',) and test.created_by != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    qs = Attempt.objects.filter(test=test, status='completed').order_by('-finished_at')
    return Response(AttemptListSerializer(qs, many=True).data)
