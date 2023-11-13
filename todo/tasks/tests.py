from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, title='Test Task')

    def test_tasks_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_complete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('complete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.get(id=self.task.id).completed)

    def test_clear_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('clear'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(user=self.user).exists())
