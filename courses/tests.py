from .models import Course
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient


class CourseAPITestCase(TestCase):
    def test_create_course(self):
        client = APIClient()
        data = {'title': 'Test Course', 'description': 'Test description'}
        response = client.post('/api/courses/', data)
        self.assertEqual(response.status_code, 201)


class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', role='instructor')
        self.client.login(username='testuser', password='testpass')

    def test_create_course(self):
        url = reverse('course-list')
        data = {'title': 'New Course', 'description': 'Course Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, 'New Course')
