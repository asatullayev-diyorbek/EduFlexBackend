from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from django.utils import timezone

from tests_app.models import Test, Question, Attempt, Answer
from users.models import User


@api_view(['GET'])
def test_analytics(request, test_pk):
    try:
        test = Test.objects.get(pk=test_pk)
    except Test.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in ('admin',) and test.created_by != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    attempts = Attempt.objects.filter(test=test, status='completed')
    count = attempts.count()
    pass_count = 0

    if count == 0:
        avg_score = 0
        avg_percentage = 0
        avg_time = 0
    else:
        agg = attempts.aggregate(
            avg_score=Avg('score'),
            avg_percentage=Avg('percentage'),
            avg_time=Avg('time_spent'),
        )
        avg_score = round(agg['avg_score'] or 0, 2)
        avg_percentage = round(agg['avg_percentage'] or 0, 1)
        avg_time = round(agg['avg_time'] or 0)
        pass_count = attempts.filter(percentage__gte=60).count()

    questions = test.questions.all()
    difficulty_analysis = []
    for q in questions:
        total_answers = Answer.objects.filter(question=q, attempt__status='completed').count()
        wrong_answers = Answer.objects.filter(question=q, attempt__status='completed', is_correct=False).count()
        error_pct = round((wrong_answers / total_answers * 100) if total_answers > 0 else 0, 1)
        difficulty_analysis.append({
            'question_id': str(q.id),
            'question_text': q.text[:80],
            'error_percentage': error_pct,
            'difficulty': q.difficulty,
        })

    pass_percentage_val = round((pass_count / count * 100) if count > 0 else 0, 1)

    return Response({
        'total_attempts': count,
        'average_score': avg_score,
        'average_percentage': avg_percentage,
        'average_time_spent': avg_time,
        'pass_percentage': pass_percentage_val,
        'difficulty_analysis': difficulty_analysis,
    })


@api_view(['GET'])
def dashboard_stats(request):
    if request.user.role != 'admin':
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    return Response({
        'total_users': User.objects.count(),
        'total_tests': Test.objects.count(),
        'total_attempts': Attempt.objects.count(),
        'active_tests': Test.objects.filter(is_active=True).count(),
        'today_attempts': Attempt.objects.filter(
            started_at__date=timezone.now().date()
        ).count(),
    })


@api_view(['GET'])
def teacher_dashboard_stats(request):
    if request.user.role not in ('teacher', 'admin'):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    tests = Test.objects.filter(created_by=request.user)
    attempts = Attempt.objects.filter(test__created_by=request.user, status='completed')

    return Response({
        'total_tests': tests.count(),
        'active_tests': tests.filter(is_active=True).count(),
        'total_attempts': attempts.count(),
        'average_score': round(attempts.aggregate(avg=Avg('percentage'))['avg'] or 0, 1),
    })


@api_view(['GET'])
def student_dashboard_stats(request):
    attempts = Attempt.objects.filter(user=request.user, status='completed')
    return Response({
        'total_attempts': attempts.count(),
        'average_score': round(attempts.aggregate(avg=Avg('percentage'))['avg'] or 0, 1),
        'tests_passed': attempts.filter(percentage__gte=60).count(),
    })
