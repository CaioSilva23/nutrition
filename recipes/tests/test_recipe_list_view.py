from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeListViewTest(RecipeTestBase):
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
        self.make_recipe().delete()
        response = self.client.get(reverse('recipe:list'))
        self.assertIn(
            'No recipes found here!',
            response.content.decode('utf-8')
        )

    def test_recipe_list_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipe:list'))
        # test context
        response_recipes = response.context['recipes']
        self.assertEqual(len(response_recipes), 1)

        # len context
        self.assertEqual(len(response_recipes), 1)

        # test content
        content = response.content.decode('utf-8')
        self.assertIn('recipe title', content)
        self.assertIn('5 Minutos', content)

    def test_recipe_home_template_dont_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipe:list"))
        self.assertIn(
           'No recipes found here!',
           response.content.decode('utf-8')
        )
