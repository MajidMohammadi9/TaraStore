from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url=reverse('login')
        cls.username='user1'
        cls.password='password1'
        CustomUser.objects.create_user(username=cls.username, password=cls.password)

    def test_login_url(self):
        response=self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response=self.client.post(self.url, {'username': self.username, 'password': self.password})     
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_unsuccess(self):
        response=self.client.post(self.url, {'username':self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        # print(response.content.decode())
        self.assertContains(response, 'Please enter a correct username and password.')


# class Logout_test(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.url=reverse('logout')
#         cls.username='user1'
#         cls.password='password1'
#         CustomUser.objects.create_user(username=cls.username, password=cls.password)

#     def test_logout(self):
#         self.client.login(username=self.username, password=self.password)
#         response=self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('home'))



class SignupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url=reverse('signup')
        cls.email='user1@gmail.com'
        cls.username='user1'
        cls.password1='tariq3170'
        cls.password2='tariq3170'

    def test_signup_url(self):
        response=self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_success(self):
        response=self.client.post(self.url, {'username': self.username, 'email': self.email, 'password1': self.password1, 'password2': self.password2})
        # print(response.content.decode())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username='user1').exists())

    def test_signup_password_mismatch(self):
        response=self.client.post(self.url, {'username': self.username, 'email': self.email, 'password1': self.password1, 'password2': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        # print(response.content.decode())
        # print(response.context['form'].errors)
        # print(response.context.keys())
        # print(response.context['form'])
        # print('form' in response.context)
        # self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')


