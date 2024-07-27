from django.urls import path
from . import views
from rest_framework.documentation import include_docs_urls
from .tokens import MyTokenObtainPairView, MyTokenRefreshView
from .views import (
    ContentListCreateAPIView,
    ContentDetailAPIView,
    QuizListCreateAPIView,
    QuizDetailAPIView,
)
urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    # path('courses/<pk>/', views.CourseDetailView.as_view()),
    # path('enrollments/', views.EnrollmentListView.as_view()),
    # path('enrollments/<pk>/', views.EnrollmentDetailView.as_view()),
    # # path('api/token/', MyTokenObtainPairView.as_view()),
    # # path('api/token/refresh/', MyTokenRefreshView.as_view()),
    # path('contents/', ContentListCreateAPIView.as_view(), name='content-list'),
    # path('contents/<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),
    # path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list'),
    # path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
]
