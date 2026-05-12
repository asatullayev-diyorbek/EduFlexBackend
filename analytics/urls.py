from django.urls import path
from . import views

urlpatterns = [
    path('analytics/tests/<int:test_pk>/', views.test_analytics, name='test-analytics'),
    path('analytics/dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('analytics/teacher/', views.teacher_dashboard_stats, name='teacher-stats'),
    path('analytics/student/', views.student_dashboard_stats, name='student-stats'),
]
