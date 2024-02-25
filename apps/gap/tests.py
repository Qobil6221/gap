from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Opinion, Comment


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('gap:login-page')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='secret')

    def test_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'secret'})
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('landing_page')) 


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('gap:register-page')

    def test_register(self):
        response = self.client.post(self.register_url,
                                    {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)

class OpinionDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.opinion = Opinion.objects.create(title='Test Opinion', body='Test body')
        self.comment = Comment.objects.create(opinion=self.opinion, author='Test Author', body='Test comment body')

    def test_get_opinion_detail(self):
        response = self.client.get(reverse('opinion-detail', kwargs={'pk': self.opinion.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gap/comments.html')
        self.assertEqual(response.context['opinion'], self.opinion)
        self.assertIn(self.comment, response.context['comments'])

    def test_get_opinion_list(self):
        response = self.client.get(reverse('opinion-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gap/rooms.html')