from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname', 'is_staff']
        read_only_fields = ['is_staff']

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
        fields = ['nickname', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'nickname': {'required': False},
        }

    def update(self, instance, validated_data):
        # 닉네임 변경
        if 'nickname' in validated_data:
            instance.nickname = validated_data.get('nickname', instance.nickname)

        # 비밀번호 변경
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        return instance