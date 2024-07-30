from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, EnrollmentSerializer
from channels.db import database_sync_to_async
from courses.permissions import IsInstructor, IsStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

# The `RegisterView` class is a Django REST framework view for creating new user registrations.


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=RegisterSerializer)
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LoginSerializer)
    # @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructorDashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsInstructor]

    async def list(self, request):
        courses = await database_sync_to_async(Course.objects.filter)(instructor=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class StudentDashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsStudent]

    async def list(self, request):
        enrollments = await database_sync_to_async(Enrollment.objects.filter)(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
