from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_staff


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'
