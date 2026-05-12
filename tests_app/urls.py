from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.test_list, name='test-list'),
    path('tests/<int:pk>/', views.test_detail, name='test-detail'),
    path('tests/<int:test_pk>/questions/', views.question_list, name='question-list'),
    path('tests/<int:test_pk>/attempts/', views.test_attempts, name='test-attempts'),
    path('questions/<int:pk>/', views.question_detail, name='question-detail'),
    path('attempts/', views.attempt_list, name='attempt-list'),
    path('attempts/<int:pk>/', views.attempt_detail, name='attempt-detail'),
    path('attempts/<int:attempt_pk>/answers/', views.submit_answer, name='submit-answer'),
    path('attempts/<int:pk>/finish/', views.finish_attempt, name='finish-attempt'),
]
