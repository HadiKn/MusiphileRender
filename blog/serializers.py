from rest_framework import serializers
from rest_framework.reverse import reverse
from users.serializers import MiniUserSerializer
from .models import BlogPost,Comment


class CommentSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    detail_url = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'detail_url']  # Add detail_url
        read_only_fields = ['id', 'created_at', 'updated_at', 'detail_url']  # Add detail_url

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('comment-detail', kwargs={'pk': obj.pk})
            )
        return None
    def create(self, validated_data):
        # Automatically set the user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BlogPostSerializer(serializers.ModelSerializer):
    author = MiniUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()
    title = serializers.CharField(
        max_length=200,
        error_messages={
            'blank': 'Title cannot be empty',
            'max_length': 'Title cannot be longer than 200 characters'
        }
    )
    content = serializers.CharField(
        max_length=1000,
        error_messages={
            'blank': 'Content cannot be empty',
            'max_length': 'Content cannot be longer than 1000 characters'
        }
    )

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'detail_url','comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at','detail_url','comments']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('blogpost-retrieve', kwargs={'pk': obj.pk})
            )
        return None

    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class MiniBlogPostSerializer(serializers.ModelSerializer):
    author = MiniUserSerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title','content', 'created_at', 'comment_count']
        read_only_fields = ['id', 'author', 'created_at', 'comment_count']    
    def get_comment_count(self, obj):
        return obj.comments.count()