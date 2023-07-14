from rest_framework import serializers
from .models import Category, Todo

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class TodoSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(source='category.name')
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Todo
        fields = '__all__'
