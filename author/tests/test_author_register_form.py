from django.test import TestCase
from parameterized import parameterized
from author.forms import RegisterForm


class AuthorRegisterFormUniTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('email', 'Your email'),
        ('password', 'Your password'),
        ('password2', 'Reapet your password'),
    ])
    def test_fields_placeholder_is_corret(self, field, placeholder):
        form = RegisterForm()
        placeholder_check = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_check, placeholder)

    @parameterized.expand([
        ('username', ('Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')),
        ('email', 'The e-mail must be valid.'),
        ('password', ('Password must have at least one uppercase letter, '
         'one lowercase letter and one number. The length should be '
         'at least 8 characters.')),

    ])
    def test_fields_help_text_is_corret(self, field, help_text):
        form = RegisterForm()
        check = form[field].field.help_text
        self.assertEqual(check, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confim password'),

    ])
    def test_fields_label_is_corret(self, field, label):
        form = RegisterForm()
        check = form[field].field.label
        self.assertEqual(check, label)
