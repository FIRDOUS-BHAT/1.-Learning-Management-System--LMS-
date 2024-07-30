from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, InstructorDashboardViewSet, StudentDashboardViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'dashboard/instructor',
                InstructorDashboardViewSet, basename='instructor-dashboard')
router.register(r'dashboard/student', StudentDashboardViewSet,
                basename='student-dashboard')


auth_urls = [
    path('register/',
         AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urls)),
]
