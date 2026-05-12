from django.contrib import admin
from .models import Test, Question, Attempt, Answer


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'question_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'type', 'difficulty', 'points', 'order_index']
    list_filter = ['type', 'difficulty']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'percentage', 'status', 'started_at']
    list_filter = ['status']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct']
