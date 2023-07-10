from django.contrib.auth.models import User
from  rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(max_length=8,write_only=True,required=True)
    password_confirmation = serializers.CharField(min_length=8,write_only=True,required=True)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password','password_confirmation')

    def validate(self,attrs):
        password_confirmation = attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError('Пароли не совпадают')

        if not attrs['first_name'].istitle():
            raise  serializers.ValidationError('Имя должно начинаться с большой буквы')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = ('id','username','first_name','last_name')