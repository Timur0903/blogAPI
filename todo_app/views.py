from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from post import permissions
from .models import Category, Todo
from .permissions import IsAuthor
from .serializers import CategorySerializer, TodoSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ('update','partial_update','destroy'):
            return [IsAuthor(), permissions.IsAuthorOrAdmin]


