from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_list_url_is_correct(self):
        url = reverse('recipe:list')
        self.assertEqual(url, '/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipe:detail', kwargs={'pk': 1})
        self.assertEqual(url, '/recipe/1/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipe:category', kwargs={'pk': 1})
        self.assertEqual(url, '/category/1/')
