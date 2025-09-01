# bible/django_bible/users/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserListView, UserManagementView, DeleteSelfView, MakeAdminView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserInfoView.as_view(), name='user-info'),
    path('me/delete/', DeleteSelfView.as_view(), name='delete-self'), # 새롭게 추가된 URL
    path('list/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/update/', UserManagementView.as_view(), name='user-update'),
    path('<int:pk>/delete/', UserManagementView.as_view(), name='user-delete'),
    path('<int:pk>/make_admin/', MakeAdminView.as_view(), name='make-admin'),
    path('manage/<int:pk>/', UserManagementView.as_view(), name='user-management'),
]