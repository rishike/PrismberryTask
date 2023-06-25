from rest_framework import serializers
from .models import Scheduler
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=True
        )
        token, created = Token.objects.get_or_create(user=user)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=False
    )
    class Meta:
        model = User
        exclude  = ['user_permissions', 'is_superuser', 'groups', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
    
    

class ScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Scheduler
        fields = ('id', 'event_name','start_date', 'end_date')
    
        
    
# class AnalyticsSerializer(serializers.Serializer):

#     class Meta:
#         model = Analytics
#         exclude = ['id', 'date', 'duration', 'scheduler']