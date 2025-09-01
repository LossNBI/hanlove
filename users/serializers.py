# bible/django_bible/users/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # is_staff와 is_active 필드를 추가하여 관리자 여부 및 활성 상태를 알 수 있게 함
        fields = ['id', 'username', 'nickname', 'is_staff', 'is_active']
        read_only_fields = ['is_staff', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'nickname']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # is_staff, is_active 필드를 추가하여 수정 가능하게 함
        fields = ['nickname', 'password', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'nickname': {'required': False},
            'is_staff': {'required': False},
            'is_active': {'required': False},
        }

    def update(self, instance, validated_data):
        # 닉네임 변경
        if 'nickname' in validated_data:
            instance.nickname = validated_data.get('nickname', instance.nickname)

        # 비밀번호 변경
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        # is_staff 필드 변경
        if 'is_staff' in validated_data:
            instance.is_staff = validated_data['is_staff']
        
        # is_active 필드 변경
        if 'is_active' in validated_data:
            instance.is_active = validated_data['is_active']

        instance.save()
        return instance
