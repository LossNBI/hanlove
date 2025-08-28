# posts/permissions.py

from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    게시물 작성자이거나 관리자(is_staff)일 때만 수정/삭제를 허용하는 커스텀 권한
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용 (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 수정 및 삭제 권한은 게시물 작성자이거나 관리자일 때만 허용
        # is_staff는 Django Admin에서 관리자 권한을 가진 사용자에게만 True입니다.
        return obj.author == request.user or request.user.is_staff

class IsCommentAuthorOrAdmin(permissions.BasePermission):
    """
    댓글 작성자이거나 관리자일 때만 수정/삭제를 허용하는 커스텀 권한
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용 (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 수정 및 삭제 권한은 댓글 작성자이거나 관리자일 때만 허용
        return obj.author == request.user or request.user.is_staff