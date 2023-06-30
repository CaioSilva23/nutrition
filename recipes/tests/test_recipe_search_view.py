from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    # view search
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipe:search'))
        self.assertIs(view.func.view_class, views.RecipeFilterView)

    def test_recipe_search_view_loads_correct_template(self):
        url = reverse('recipe:search') + '?search=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')

    def test_recipe_search_raises_404_if_not_search_term(self):
        response = self.client.get(reverse('recipe:search'))
        self.assertEqual(response.status_code, 404)
