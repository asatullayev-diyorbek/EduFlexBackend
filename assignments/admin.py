from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Assignment, AssignmentTask, Submission, TaskResponse


class AssignmentTaskInline(TabularInline):
    model = AssignmentTask
    extra = 0
    fields = ['order', 'task_type', 'question_text', 'max_score']
    show_change_link = True


class TaskResponseInline(TabularInline):
    model = TaskResponse
    extra = 0
    fields = ['task', 'response_text', 'score', 'auto_graded', 'grader_feedback']
    readonly_fields = ['task', 'response_text', 'auto_graded']


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display  = ['title', 'teacher', 'task_type', 'is_published', 'deadline', 'tasks_count', 'submissions_count', 'created_at']
    list_filter   = ['is_published', 'task_type']
    search_fields = ['title', 'description', 'teacher__email']
    ordering      = ['-created_at']
    list_per_page = 20
    list_select_related = ['teacher']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AssignmentTaskInline]

    fieldsets = (
        ('Asosiy', {'fields': ('title', 'description', 'instructions', 'teacher')}),
        ('Sozlamalar', {'fields': ('task_type', 'max_score', 'deadline', 'is_published')}),
        ('Sana', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(AssignmentTask)
class AssignmentTaskAdmin(ModelAdmin):
    list_display  = ['assignment', 'order', 'task_type', 'question_text', 'max_score']
    list_filter   = ['task_type']
    search_fields = ['question_text', 'assignment__title']
    ordering      = ['assignment', 'order']
    list_per_page = 30
    list_select_related = ['assignment']


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display  = ['student', 'assignment', 'status', 'score', 'max_score', 'percentage', 'submitted_at']
    list_filter   = ['status']
    search_fields = ['student__email', 'student__name', 'assignment__title']
    ordering      = ['-created_at']
    list_per_page = 25
    list_select_related = ['student', 'assignment']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    inlines = [TaskResponseInline]

    fieldsets = (
        ('Topshiriq', {'fields': ('student', 'assignment', 'status')}),
        ('Natija', {'fields': ('score', 'max_score', 'feedback')}),
        ('Vaqt', {'fields': ('submitted_at', 'created_at', 'updated_at')}),
    )


@admin.register(TaskResponse)
class TaskResponseAdmin(ModelAdmin):
    list_display  = ['submission', 'task', 'score', 'auto_graded', 'grader_feedback']
    list_filter   = ['auto_graded']
    search_fields = ['submission__student__email']
    ordering      = ['submission']
    list_per_page = 30
    list_select_related = ['submission', 'task']
