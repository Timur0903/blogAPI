from rest_framework import serializers
from .models import Like, Favorites


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if user.likes.filer(post=post).exists():
            raise serializers.ValidationError(
                'you already liked this post!'
            )
        return attrs

class FavoritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'post')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_title'] = instance.post.title
        if instance.post.preview:
            preview = instance.pos.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation


