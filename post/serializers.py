from rest_framework import serializers, generics
from comment.serializers import CommentSerializer
from like.models import Like
from like.serializers import LikeSerializer
from category.models import Category
from .models import Post, PostImages


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview', 'owner_name', 'category_name')

class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        required=True,queryset=Category.objects.all()
    )
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')

        for image in images_data:
            PostImages.objects.create(image=image,post=post)

        return post

class PostDetailsSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)


    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    @staticmethod
    def is_liked(post, user):
        return user.favorite.filter(post=post).exists()



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity of likes'] = 0
        for i in representation['likes']:
            representation['quantity of likes'] += 1
        representation['comments_count'] = instance.comments.count()
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance, user)
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation

class LikedUsersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['owner', 'owner_username']

