from parameterized import parameterized
from author.forms import RegisterForm
from test_author_base import AuthorTestBase


class AuthorRegisterFormUniTest(AuthorTestBase):
    """test unitary"""
    @parameterized.expand([
        ('username', 'Your username'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('email', 'Your email'),
        ('password', 'Your password'),
        ('password2', 'Reapet your password'),
    ])
    def test_field_placeholder_is_corret(self, field, placeholder):
        """Test placeholder fields"""
        form = RegisterForm()
        placeholder_check = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_check, placeholder)

    @parameterized.expand([
        ('username', ('Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')),  # noqa: E501
        ('email', 'The e-mail must be valid.'),
        ('password', ('Password must have at least one uppercase letter, '
                    'one lowercase letter and one number. The length should be '
                    'at least 8 characters.')),
    ])
    def test_field_help_text_is_corret(self, field, help_text):
        """Test help_text fields"""
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
    def test_field_label_is_corret(self, field, label):
        """Test label fields"""
        form = RegisterForm()
        check = form[field].field.label
        self.assertEqual(check, label)


class AuthorRegisterIntegrationTest(AuthorTestBase):
    """Test integration"""
    @parameterized.expand([
            ('username', 'This field is required.'),
            ('first_name', 'This first name is required'),
            ('last_name', 'This last name is required'),
            ('email', 'This email is required'),
            ('password', 'Password must not be empty'),
            ('password2', 'Please, reapet your password')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        """form fields cannot be empty"""
        self.form_data[field] = ''
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_has_less_than_4_characters(self):
        """testing if the field has less than 4 characters"""
        self.form_data['username'] = 'ada'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        msg = 'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui 3).'  # noqa: E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertEqual([msg], response.context['form'].errors.get('username'))  # noqa: E501

    def test_username_has_more_than_150_characters(self):
        """testing if the field has more than 150 characters"""
        self.form_data['username'] = 'a' * 151
        response = self.client.post(self.url, data=self.form_data, follow=True)

        msg = 'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui 151).'  # noqa: E501
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertEqual([msg], response.context['form'].errors.get('username'))  # noqa: E501

    def test_password_is_not_equal(self):
        """testing password not equal"""
        self.form_data['password'] = 'Caiokaiak@1'
        self.form_data['password2'] = 'Caiokaiak@1a'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        msg = 'The entered passwords are not the same'  # noqa: E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_is_not_valid(self):
        """testing password is not valid"""
        self.form_data['password'] = 'abc123'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'  # noqa: E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    # def test_field_email_already_exists(self):

    #     user = RegisterForm(data=self.form_data)

    #     self.form_data['email'] = 'email@mail.com'

    #     response = self.client.post(self.url, data=self.form_data, follow=True)
    #     msg = 'User with this email already exists'

    #     self.assertIn(msg, response.context['email'].errors.get('email'))
