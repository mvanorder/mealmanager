from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe


class TestRecipe(TestCase):

    def test_00_create_recipe_fail(self):
        """
        Ensure that creating a recipe without a name will fail.
        :return:
        """
        client = Client()
        post_data = {
            'recipe-directions': 'bar',
            'ingredient_0-quantity_amount': '1 1/2',
            'ingredient_0-ingredient': 'flour',
            'ingredient_1-quantity_amount': '2',
            'ingredient_1-ingredient': 'eggs'
        }
        response = client.post('/recipes/create', post_data)
        self.assertContains(response, 'This field is required', status_code=200)

    def test_01_create_and_get_recipe(self):
        """
        Ensure a recipe can be created and retrieved
        :return:
        """
        client = Client()
        post_data = {
            'recipe-name': 'foo',
            'recipe-directions': 'bar',
            'ingredient_0-quantity_amount': '1 1/2',
            'ingredient_0-ingredient': 'flour',
            'ingredient_1-quantity_amount': '2',
            'ingredient_1-ingredient': 'eggs'
        }
        response = client.post('/recipes/create', post_data)
        self.assertRedirects(
            response,
            '/recipes/1',
            status_code=302,
            target_status_code=200,
            host=None,
            msg_prefix='',
            fetch_redirect_response=True)
        self.assertTrue(Recipe.objects.get(name='foo'))
        recipe = Recipe.objects.get(name='foo')
        self.assertEqual(len(recipe.recipe_ingredients), 2)

        response = client.get(reverse('recipes.views.recipe_view', args=[str(recipe.id)]))
        self.assertEqual(response.context['recipe'].name, post_data['recipe-name'])
        self.assertEqual(response.context['recipe'].directions, post_data['recipe-directions'])
        self.assertEqual(len(response.context['recipe_ingredients']), 2)

    @skip('Need to detect the form error properly')
    def test_02_create_recipe_invalid(self):
        client = Client()
        post_data = {
            'recipe-name': 'foo',
            'recipe-directions': 'bar',
            'ingredient_0-quantity_amount': '1 1 1/2',
            'ingredient_0-ingredient': 'flour',
        }
        response = client.post('/recipes/create', post_data)
        self.assertRedirects(
            response,
            '/recipes/1',
            status_code=302,
            target_status_code=200,
            host=None,
            msg_prefix='',
            fetch_redirect_response=True)
        recipe = Recipe.objects.get(name='foo')
        self.assertContains(response, 'Quantity is not a valid number or fraction.', status_code=302)
