from rest_framework import serializers
from .models import Question, Answer
from accounts.models import User


class QuestionListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Question
        fields = ('id', 'user_seq', 'username', 'title', 'content', 'created_at', 'location_seq')



class AnswerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('user_seq', 'question_seq', 'route_seq_id', 'username',)


class QuestinoSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source='answers.all')
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('user_seq','location_seq','username')

