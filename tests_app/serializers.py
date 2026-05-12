from rest_framework import serializers
from .models import Test, Question, Attempt, Answer


class QuestionSerializer(serializers.ModelSerializer):
    test_id = serializers.PrimaryKeyRelatedField(source='test', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'test_id', 'text', 'type', 'data',
            'explanation', 'difficulty', 'points', 'time_limit', 'order_index',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['test_id'] = str(instance.test_id)
        rep['id'] = str(instance.id)
        return rep


class TestSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Test
        fields = [
            'id', 'title', 'description', 'created_by',
            'time_limit', 'is_active', 'randomize_questions',
            'randomize_options', 'show_feedback', 'created_at', 'updated_at',
            'question_count',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        rep['created_by'] = str(instance.created_by_id)
        return rep


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(source='question', read_only=True)
    attempt_id = serializers.PrimaryKeyRelatedField(source='attempt', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'attempt_id', 'question_id', 'user_answer', 'is_correct', 'points_earned', 'answered_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        rep['attempt_id'] = str(instance.attempt_id)
        rep['question_id'] = str(instance.question_id)
        return rep


class AttemptSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(source='test', read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Attempt
        fields = [
            'id', 'user_id', 'test_id', 'score', 'max_score',
            'percentage', 'status', 'started_at', 'finished_at', 'time_spent', 'answers',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        rep['user_id'] = str(instance.user_id)
        rep['test_id'] = str(instance.test_id)
        return rep


class AttemptListSerializer(AttemptSerializer):
    """Attempt list without answers for performance."""
    class Meta(AttemptSerializer.Meta):
        fields = [
            'id', 'user_id', 'test_id', 'score', 'max_score',
            'percentage', 'status', 'started_at', 'finished_at', 'time_spent',
        ]
