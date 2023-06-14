from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    # recipe detail
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:detail', kwargs={'slug': 'slug'}))
        self.assertIs(view.func, views.recipe_detail)

    def test_recipe_detail_view_return_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipe:detail', kwargs={'slug': 'slug'}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        self.make_recipe(title="Ola teste")
        response = self.client.get(reverse('recipe:category', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn('Ola teste', content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipe:detail', kwargs={'slug':recipe.slug}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_loads_correct_template(self):
        recipe = self.make_recipe(title='teste detail')
        response = self.client.get(reverse('recipe:detail', kwargs={'slug':recipe.slug}))
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
