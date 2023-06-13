from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    # recipe list
    def test_recipe_list_view_function_is_correct(self):
        view = resolve(reverse('recipe:list'))
        self.assertIs(view.func, views.recipe_list)

    def test_recipe_list_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipe:list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view_loads_correct_template(self):
        response = self.client.get(reverse('recipe:list'))
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_list_template_shows_no_recipe_found_if_no_recipe(self):
        response = self.client.get(reverse('recipe:list'))
        self.assertIn(
            'No recipes found here!',
            response.content.decode('utf-8')
        )
    def test_recipe_home_template_loads_recipes(self):
        ...    

    # recipe detai
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:detail', kwargs={'pk': 1}))
        self.assertIs(view.func, views.recipe_detail)

    def test_recipe_detail_view_return_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipe:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    # recipe detail
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'pk': 1000}))
        self.assertIs(view.func, views.category_list)

    def test_recipe_category_view_return_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipe:category', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

 