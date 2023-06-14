from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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
        self.assertEqual(response_recipes.first().title, 'recipe title')

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
        
    # recipe category
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'pk': 1000}))
        self.assertIs(view.func, views.recipe_list_category)

    def test_recipe_category_view_return_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipe:category', kwargs={'pk': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipe(self):
        self.make_recipe(title="Ola teste")
        response = self.client.get(reverse('recipe:category', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn('Ola teste', content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipe:category', kwargs={'pk':recipe.category.pk}))
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
       


