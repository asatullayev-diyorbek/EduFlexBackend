from django.db import models
from django.conf import settings


class Assignment(models.Model):
    TASK_TYPE_CHOICES = [
        ('short_answer', 'Short Answer'),
        ('code',         'Code Task'),
        ('file_upload',  'File Upload'),
        ('mixed',        'Mixed'),
    ]

    title         = models.CharField(max_length=255)
    description   = models.TextField(blank=True)
    instructions  = models.TextField(blank=True)
    task_type     = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='short_answer')
    teacher       = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments'
    )
    deadline      = models.DateTimeField(null=True, blank=True)
    max_score     = models.PositiveIntegerField(default=100)
    is_published  = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def tasks_count(self):
        return self.tasks.count()

    @property
    def submissions_count(self):
        return self.submissions.count()


class AssignmentTask(models.Model):
    TASK_TYPES = [
        ('short_answer', 'Short Answer'),
        ('code',         'Code Task'),
        ('file_upload',  'File Upload'),
    ]

    assignment    = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='tasks')
    order         = models.PositiveIntegerField(default=0)
    task_type     = models.CharField(max_length=20, choices=TASK_TYPES, default='short_answer')
    question_text = models.TextField()
    max_score     = models.PositiveIntegerField(default=10)
    # short_answer: {"answer_pattern": "regex", "case_sensitive": false, "sample_answer": "..."}
    # code:         {"language": "python", "starter_code": "...", "test_cases": [...]}
    # file_upload:  {"allowed_types": ["pdf","docx"], "max_size_mb": 10}
    config        = models.JSONField(default=dict)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.assignment.title} — task {self.order}"


class Submission(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('submitted', 'Submitted'),
        ('graded',    'Graded'),
    ]

    student      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions'
    )
    assignment   = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    score        = models.FloatField(null=True, blank=True)
    max_score    = models.FloatField(null=True, blank=True)
    feedback     = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'assignment')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.name} — {self.assignment.title}"

    @property
    def percentage(self):
        if self.max_score and self.max_score > 0 and self.score is not None:
            return round(self.score / self.max_score * 100, 1)
        return None


class TaskResponse(models.Model):
    submission      = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='responses')
    task            = models.ForeignKey(AssignmentTask, on_delete=models.CASCADE, related_name='responses')
    response_text   = models.TextField(blank=True)
    score           = models.FloatField(null=True, blank=True)
    auto_graded     = models.BooleanField(default=False)
    grader_feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('submission', 'task')
