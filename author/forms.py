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

    first_name = forms.CharField(label='First name', required=True)

    last_name = forms.CharField(
        label='Last name',
        required=True,
    )

    username = forms.CharField(
        label='Username',
        required=True,
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
        )

    email = forms.EmailField(
        label='E-mail',
        required=True,
        help_text='The e-mail must be valid.'
        )

    password = forms.CharField(
        label='Password',
        required=True,
        validators=[strong_password],
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
        # error_messages={
        #     'required': 'Password must not be empty'
        # },
        # help_text=(
        #     'Password must have at least one uppercase letter, '
        #     'one lowercase letter and one number. The length should be '
        #     'at least 8 characters.'
        # )
    )

    password2 = forms.CharField(
        label='Confim password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Reapet your password'}))

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
            raise ValidationError('User with this email already exists', code='invalid')
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
