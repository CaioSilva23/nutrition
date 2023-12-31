from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_default(self):
        recipe = self.make_recipe(
            author_data={'username': 'teste'},
            category_data={'name': 'category'},
            slug='dsaad',
            is_published=False,
            )

        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ("title", 65),
        ("description", 165),
        ("preparation_time_unit", 65),
        ("servings_unit", 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() 

    def test_recipe_string_represetantion(self):
        self.assertEqual(str(self.recipe), self.recipe.title)
