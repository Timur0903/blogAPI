from rest_framework import serializers, generics
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
        fields = ('id','title','owner','category','preview','owner_name','category_name')

class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        required=True,queryset=Category.objects.all()
    )
    images = PostImageSerializer(many=True,required=False)

    class Meta:
        model = Post
        fields = ('title', 'body','category','preview','images')

    def create(self,validated_data):
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity of likes'] = 0
        for i in representation['likes']:
            representation['quantity of likes'] += 1
        return representation