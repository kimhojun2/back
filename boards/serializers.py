from rest_framework import serializers
from .models import Board, Comment
from accounts.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username')


class BoardListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Board
        fields = ('id', 'user_seq', 'username', 'title', 'content', 'created_at')




# class CommentListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('id', 'user_seq', 'board_seq', 'created_at', 'updated_at', 'is_deleted')


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user_seq', 'board_seq','username')


class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='comments.all')
    username = serializers.ReadOnlyField(source='user_seq.username')
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('user_seq','username',)

