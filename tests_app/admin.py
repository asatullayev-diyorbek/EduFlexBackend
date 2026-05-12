from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Test, Question, Attempt, Answer


class QuestionInline(TabularInline):
    model = Question
    extra = 0
    fields = ['text', 'type', 'difficulty', 'points', 'order_index']
    show_change_link = True


class AnswerInline(TabularInline):
    model = Answer
    extra = 0
    fields = ['question', 'is_correct', 'points_earned']
    readonly_fields = ['question', 'is_correct', 'points_earned']
    can_delete = False


@admin.register(Test)
class TestAdmin(ModelAdmin):
    list_display  = ['title', 'created_by', 'is_active', 'question_count', 'time_limit', 'created_at']
    list_filter   = ['is_active', 'randomize_questions']
    search_fields = ['title', 'description']
    ordering      = ['-created_at']
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]

    fieldsets = (
        ('Asosiy', {'fields': ('title', 'description', 'created_by')}),
        ('Sozlamalar', {'fields': ('time_limit', 'is_active', 'randomize_questions', 'randomize_options', 'show_feedback')}),
        ('Sana', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display  = ['text', 'test', 'type', 'difficulty', 'points', 'order_index']
    list_filter   = ['type', 'difficulty']
    search_fields = ['text']
    ordering      = ['test', 'order_index']
    list_per_page = 30
    list_select_related = ['test']


@admin.register(Attempt)
class AttemptAdmin(ModelAdmin):
    list_display  = ['user', 'test', 'score', 'percentage', 'status', 'started_at', 'finished_at']
    list_filter   = ['status']
    search_fields = ['user__email', 'user__name', 'test__title']
    ordering      = ['-started_at']
    list_per_page = 25
    list_select_related = ['user', 'test']
    readonly_fields = ['started_at', 'finished_at', 'time_spent']
    inlines = [AnswerInline]

    fieldsets = (
        ('Urinish', {'fields': ('user', 'test', 'status')}),
        ('Natija', {'fields': ('score', 'max_score', 'percentage')}),
        ('Vaqt', {'fields': ('started_at', 'finished_at', 'time_spent')}),
    )


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display  = ['attempt', 'question', 'is_correct', 'points_earned', 'answered_at']
    list_filter   = ['is_correct']
    search_fields = ['attempt__user__email']
    ordering      = ['-answered_at']
    list_per_page = 30
    list_select_related = ['attempt', 'question']
    readonly_fields = ['answered_at']
