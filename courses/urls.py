from django.urls import path
from . import views
from rest_framework.documentation import include_docs_urls
from .tokens import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    path('courses/<pk>/', views.CourseDetailView.as_view()),
    path('students/', views.StudentListView.as_view()),
    path('students/<pk>/', views.StudentDetailView.as_view()),
    path('enrollments/', views.EnrollmentListView.as_view()),
    path('enrollments/<pk>/', views.EnrollmentDetailView.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view()),
    path('api/token/refresh/', MyTokenRefreshView.as_view()),
]
