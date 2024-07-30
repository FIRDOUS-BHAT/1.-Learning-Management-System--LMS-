from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView, EnrollmentListCreateAPIView, EnrollmentDetailAPIView, ContentListCreateAPIView, ContentDetailAPIView, QuizListCreateAPIView, QuizDetailAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('enrollments/', EnrollmentListCreateAPIView.as_view(),
         name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailAPIView.as_view(),
         name='enrollment-detail'),
    path('contents/', ContentListCreateAPIView.as_view(), name='content-list'),
    path('contents/<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),
    path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
]
