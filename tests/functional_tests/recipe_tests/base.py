from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from recipes.tests.test_recipe_base import RecipeMixin


class RecipeBaseTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_driver()  # '--headless'
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
