# posts/permissions.py

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    게시물의 작성자만 수정 및 삭제를 허용하는 커스텀 권한
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 요청(GET, HEAD, OPTIONS)은 모든 사용자에게 허용합니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 요청(PUT, PATCH, DELETE)은 작성자만 허용합니다.
        return obj.author == request.user

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    작성자 또는 관리자만 수정 및 삭제를 허용하는 커스텀 권한
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 요청(GET, HEAD, OPTIONS)은 모든 사용자에게 허용합니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 요청(PUT, PATCH, DELETE)은 작성자 또는 관리자만 허용합니다.
        return obj.author == request.user or request.user.is_superuser