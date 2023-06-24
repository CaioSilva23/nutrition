from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorTestBase(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'user',
            'last_name': 'last',
            'email': 'email@mail.com',
            'password': 'Caiokaiak@1',
            'password2': 'Caiokaiak@1'
        }

        self.url = reverse('author:register')
        return super().setUp()

    def make_author(
            self,
            first_name='user',
            last_name='user',
            username='user',
            password='user123',
            email='user@mail.com',
            ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email)
