# # from django.test import LiveServerTestCase
# from selenium.webdriver.common.by import By
# from .base import RecipeBaseTest
# from time import sleep
# import pytest


# @pytest.mark.functional_test
# class RecipeListPageFuncionalTest(RecipeBaseTest):
#     def test_recipe_list_page_without_recipes_found_message(self):
#         browser = self.browser
#         browser.get(self.live_server_url)
#         body = browser.find_element(By.TAG_NAME, 'body')
#         self.assertIn('No recipes found here!', body.text)

#     def test_recipe_list_page_without_recipes(self):
#         self.make_recipe_in_batch()
#         browser = self.browser
#         browser.get(self.live_server_url)
#         body = browser.find_element(By.TAG_NAME, 'body')
#         self.assertNotIn('No recipes found here!', body.text)
