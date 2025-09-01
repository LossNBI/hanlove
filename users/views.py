# bible/django_bible/users/views.py

import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer
from rest_framework import permissions
from django.db import transaction

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)

# 회원가입
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'nickname': user.nickname,
                'is_staff': user.is_staff
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 내 정보 조회
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 사용자 목록 조회 (관리자 전용)
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all().order_by('id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 관리자용 사용자 관리 (비밀번호, is_staff, is_active 변경 등)
class UserManagementView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            # --- 디버그 로그 시작 ---
            logger.debug(f"PUT 요청이 도착했습니다. PK: {pk}")
            logger.debug(f"요청 데이터: {request.data}")
            # --- 디버그 로그 끝 ---

            # 트랜잭션으로 데이터 무결성 보장
            with transaction.atomic():
                user = CustomUser.objects.get(pk=pk)

                # 슈퍼유저는 다른 관리자를 수정할 수 없습니다.
                if user.is_superuser and not request.user.is_superuser:
                    logger.warning("슈퍼유저가 아닌 사용자가 슈퍼유저를 관리하려 함")
                    return Response({'error': 'You cannot manage a superuser.'}, status=status.HTTP_403_FORBIDDEN)
                
                # 자기 자신은 관리자 권한을 해제할 수 없도록 방지
                if user == request.user and 'is_staff' in request.data and not request.data['is_staff']:
                    logger.warning(f"사용자({request.user.username})가 자신의 관리자 권한을 해제하려 함.")
                    return Response({'error': 'You cannot dismiss yourself from admin role.'}, status=status.HTTP_403_FORBIDDEN)
                
                # is_staff와 is_active 필드 업데이트를 허용
                serializer = UserUpdateSerializer(user, data=request.data, partial=True)
                
                # --- 디버그 로그 시작 ---
                if not serializer.is_valid():
                    logger.debug(f"유효성 검사 실패! 오류: {serializer.errors}")
                else:
                    logger.debug("유효성 검사 통과. 데이터를 저장합니다.")
                # --- 디버그 로그 끝 ---
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            logger.error(f"사용자를 찾을 수 없습니다. PK: {pk}")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"예상치 못한 오류 발생: {e}", exc_info=True)
            return Response({'error': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_staff and not request.user.is_superuser:
            return Response({'error': 'You cannot delete another admin user.'}, status=status.HTTP_403_FORBIDDEN)
            
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 자기 계정 삭제 (사용자 전용)
class DeleteSelfView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 관리자 임명
class MakeAdminView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_staff = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
