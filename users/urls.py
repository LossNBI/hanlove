# bible/django_bible/users/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserListView, UserManagementView, DeleteSelfView

urlpatterns = [
    # 회원가입 및 로그인
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # 내 계정 관리
    path('me/', UserInfoView.as_view(), name='user-info'),
    path('me/delete/', DeleteSelfView.as_view(), name='delete-self'),
    
    # 관리자 전용 사용자 목록 조회
    path('list/', UserListView.as_view(), name='user-list'),

    # 단일 URL로 모든 관리자 작업 처리
    # 이 URL을 사용하여 비밀번호 변경, 관리자 임명/해임, 계정 삭제 등을 처리합니다.
    path('manage/<int:pk>/', UserManagementView.as_view(), name='user-management'),
    
    # make_admin 같은 중복된 URL은 삭제하는 것이 좋습니다.
    # Flutter 앱의 makeUserAdmin과 removeUserAdmin 함수도 이 URL로 통일해야 합니다.
]