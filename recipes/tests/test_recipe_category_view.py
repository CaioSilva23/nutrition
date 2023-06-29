from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    # recipe category
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'name': 'Carnes'}))
        self.assertIs(view.func, views.recipe_list_category)

    def test_recipe_category_view_return_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipe:category', kwargs={'name': 'Carnes'}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipe(self):
        self.make_recipe(title="Ola teste")
        response = self.client.get(reverse('recipe:category', args=('Category',)))
        content = response.content.decode('utf-8')
        self.assertIn('Ola teste', content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipe:category', kwargs={'name': recipe.category.name}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    # view search
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipe:search'))
        self.assertIs(view.func, views.recipes_search)

    def test_recipe_search_view_loads_correct_template(self):
        url = reverse('recipe:search') + '?search=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')

    def test_recipe_search_raises_404_if_not_search_term(self):
        response = self.client.get(reverse('recipe:search'))
        self.assertEqual(response.status_code, 404)

