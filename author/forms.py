from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.strong_password import strong_password


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')
        add_placeholder(self.fields['email'], 'Your email')

    first_name = forms.CharField(
        min_length=4,
        max_length=150,
        label='First name',
        error_messages={'required': 'This first name is required'})

    last_name = forms.CharField(
        min_length=4,
        max_length=150,
        label='Last name',
        error_messages={'required': 'This last name is required'})

    username = forms.CharField(
        min_length=4,
        max_length=150,
        label='Username',
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',  # noqa: E501
        error_messages={'required': 'This field is required.'}
        )

    email = forms.EmailField(
        label='E-mail',
        help_text='The e-mail must be valid.',
        error_messages={'required': 'This email is required'}
        )

    password = forms.CharField(
        label='Password',
        validators=[strong_password],
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={'required': 'Password must not be empty'},
        # help_text=(
        #     'Password must have at least one uppercase letter, '
        #     'one lowercase letter and one number. The length should be '
        #     'at least 8 characters.'
        # )
    )

    password2 = forms.CharField(
        label='Confim password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Reapet your password'}),  # noqa: E501
        error_messages={'required': 'Please, reapet your password'}
        )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
            )
    # valida um campo unico (clean + nome do campo)
    # def clean_password(self):
    #     data = self.cleaned_data['password']
    #     return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise ValidationError('User with this email already exists', code='invalid')  # noqa: E501
        return email

    def clean(self) -> Dict[str, Any]:
        password = self.cleaned_data.get('password')
        if password:
            password2 = self.cleaned_data.get('password2')
            if password != password2:
                error_password = ValidationError(
                                    'The entered passwords are not the same',
                                    code='invalid')
                raise ValidationError({
                    'password': error_password,
                    'password2': error_password
                })
        return super().clean()
