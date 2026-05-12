from rest_framework import serializers
from .models import Assignment, AssignmentTask, Submission, TaskResponse


class AssignmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AssignmentTask
        fields = ['id', 'order', 'task_type', 'question_text', 'max_score', 'config']


class AssignmentListSerializer(serializers.ModelSerializer):
    teacher_name    = serializers.CharField(source='teacher.name', read_only=True)
    tasks_count     = serializers.IntegerField(read_only=True)
    submissions_count = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Assignment
        fields = [
            'id', 'title', 'description', 'task_type', 'teacher_name',
            'deadline', 'max_score', 'is_published',
            'tasks_count', 'submissions_count', 'created_at',
        ]


class AssignmentDetailSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    tasks        = AssignmentTaskSerializer(many=True, read_only=True)

    class Meta:
        model  = Assignment
        fields = [
            'id', 'title', 'description', 'instructions', 'task_type',
            'teacher_name', 'deadline', 'max_score', 'is_published',
            'tasks', 'created_at', 'updated_at',
        ]


class AssignmentCreateSerializer(serializers.ModelSerializer):
    tasks = AssignmentTaskSerializer(many=True, required=False)

    class Meta:
        model  = Assignment
        fields = [
            'id', 'title', 'description', 'instructions', 'task_type',
            'deadline', 'max_score', 'is_published', 'tasks',
        ]

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        assignment = Assignment.objects.create(**validated_data)
        for i, task_data in enumerate(tasks_data):
            task_data.setdefault('order', i)
            AssignmentTask.objects.create(assignment=assignment, **task_data)
        return assignment

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tasks_data is not None:
            instance.tasks.all().delete()
            for i, task_data in enumerate(tasks_data):
                task_data.setdefault('order', i)
                AssignmentTask.objects.create(assignment=instance, **task_data)
        return instance


class TaskResponseSerializer(serializers.ModelSerializer):
    task_id       = serializers.IntegerField(source='task.id', read_only=True)
    task_type     = serializers.CharField(source='task.task_type', read_only=True)
    question_text = serializers.CharField(source='task.question_text', read_only=True)
    max_score     = serializers.IntegerField(source='task.max_score', read_only=True)

    class Meta:
        model  = TaskResponse
        fields = [
            'id', 'task_id', 'task_type', 'question_text', 'max_score',
            'response_text', 'score', 'auto_graded', 'grader_feedback',
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_email= serializers.CharField(source='student.email', read_only=True)
    responses    = TaskResponseSerializer(many=True, read_only=True)
    percentage   = serializers.FloatField(read_only=True)

    class Meta:
        model  = Submission
        fields = [
            'id', 'student_name', 'student_email', 'status',
            'submitted_at', 'score', 'max_score', 'percentage',
            'feedback', 'responses', 'created_at', 'updated_at',
        ]


class SubmissionListSerializer(serializers.ModelSerializer):
    student_name  = serializers.CharField(source='student.name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    percentage    = serializers.FloatField(read_only=True)

    class Meta:
        model  = Submission
        fields = [
            'id', 'student_name', 'student_email', 'status',
            'submitted_at', 'score', 'max_score', 'percentage', 'feedback',
        ]
