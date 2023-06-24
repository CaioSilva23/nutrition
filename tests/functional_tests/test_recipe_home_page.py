# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from selenium.webdriver.common.by import By
from time import sleep


class RecipeBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_driver('--headless')
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()


class RecipeListPageFuncionalTest(RecipeBaseTest):
    def setUp(self) -> None:
        return super().setUp()

    def test_the_test(self):
        browser = self.browser
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here!', body.text)
