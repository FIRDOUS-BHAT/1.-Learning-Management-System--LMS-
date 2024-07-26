from django.test import TestCase
from rest_framework.test import APIClient
from .models import Course, Student, Enrollment


class CourseAPITestCase(TestCase):
    def test_create_course(self):
        client = APIClient()
        data = {'title': 'Test Course', 'description': 'Test description'}
        response = client.post('/api/courses/', data)
        self.assertEqual(response.status_code, 201)
