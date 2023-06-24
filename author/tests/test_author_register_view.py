from test_author_base import AuthorTestBase


class AuthorRegisterViewTest(AuthorTestBase):
    def test_send_get_registration_register_view(self):
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_send_post_registration_register_view(self):
        url = self.url
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_email_user_exists(self):
        url = self.url
        data1 = self.form_data
        data2 = self.form_data
        self.client.post(url, data=data1, follow=True)
        response = self.client.post(url, data=data2, follow=True)
        msg = 'User with this email already exists'
        self.assertIn(msg, response.context['form'].errors.get('email'))
