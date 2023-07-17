from django.shortcuts import render
from rest_framework import generics, permissions

from comment.serializers import CommentSerializer
from like.models import Favorites
from .models import Post
from .permissions import IsAuthorOrAdmin, IsAuthor
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailsSerializer, LikedUsersSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.



# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return PostCreateSerializer
#         return PostListSerializer
#
# class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset =  Post.objects.all()
#     lookup_fields = 'id'
#     def get_permissions(self):
#         if self.request.method == 'DELETE':
#             return IsAuthorOrAdmin(),
#         elif self.request.method in ['PUT','PATCH']:
#             return IsAuthor(),
#         return permissions.AllowAny(),
#
#     def get_serializer_class(self):
#         if self.request.method in ['PUT','PATCH']:
#             return PostCreateSerializer
#         return PostDetailsSerializer
#
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return PostDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]

        # elif self.action in ('update','partial_update'):
        #     return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticatedOrReadOnly(), ]


    #localhost:8000/post/1/like/
    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikedUsersSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # localhost:8000/post/id/comment/
    @action(['GET'], detail=True)
    def comment(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method =='POST':
            if user.favotites.filter(post=post).exists():
                return Response ('Tы уже добавил этот пост', status=400)
            Favorites.objects.create(owner=user, post=post)
            return Response('Добавлено в избранное',status=201)
        else:
            favorite = user.favotites.filter(post=post)
            if favorite.exists():
                favorite.delete()
                return Response('Ты удалил этот пост из избранного', status=204)
            return Response('Пост не найден', status=404)
