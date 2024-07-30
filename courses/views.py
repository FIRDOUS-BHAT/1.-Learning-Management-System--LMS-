from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment, Content, Quiz, Question, Choice, Submission
from .serializers import CourseSerializer, EnrollmentSerializer, ContentSerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer, SubmissionSerializer
from .permissions import IsInstructor, IsStudent
from asgiref.sync import async_to_sync


from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsInstructor
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from notifications.utils import send_notification_email


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    async def perform_create(self, serializer):
        course = await database_sync_to_async(serializer.save)(instructor=self.request.user)
        # Send a notification to the user
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f"user_{self.request.user.id}",
            {
                "type": "notification_message",
                "message": f"A new course '{course.title}' has been created."
            }
        )

        # Send email notification
        send_notification_email(
            "New Course Created",
            f"A new course '{course.title}' has been created by {self.request.user.email}.",
            [self.request.user.email]
        )


class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EnrollmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Enrollment, pk=pk)

    def get(self, request, pk):
        enrollment = self.get_object(pk)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def delete(self, request, pk):
        enrollment = self.get_object(pk)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    def get(self, request):
        contents = Content.objects.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            course = get_object_or_404(Course, pk=request.data.get('course'))
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Content, pk=pk)

    def get(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Quiz, pk=pk)

    def get(self, request, pk):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, pk):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        quiz = self.get_object(pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
