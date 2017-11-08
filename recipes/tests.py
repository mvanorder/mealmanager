from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse
from .models import Ingredient, Quantity, QuantityType, Recipe, RecipeIngredient


class TestRecipe(TestCase):

    def setUp(self):
        """Set up for testing recipes.
        """
        quantity_types = [
            {
                'name': 'count'
            },
            {
                'name': 'volume'
            },
            {
                'name': 'weight'
            }
        ]

        for quantity_type in quantity_types:
            QuantityType.objects.create(**quantity_type)

        count = QuantityType.objects.get(name='count')
        volume = QuantityType.objects.get(name='volume')

        quantities = [
            {
                'name': 'count',
                'scale': '1',
                'quantity_type': count
            },
            {
                'name': 'dozen',
                'scale': '12',
                'quantity_type': count
            },
            {
                'name': 'Dash',
                'scale': '1/16',
                'quantity_type': volume
            },
            {
                'name': 'Pinch',
                'scale': '1/8',
                'quantity_type': volume
            },
            {
                'name': 'Teaspoon',
                'scale': '1',
                'quantity_type': volume
            },
            {
                'name': 'Tablespoon',
                'scale': '3',
                'quantity_type': volume
            },
            {
                'name': 'Fluid ounce',
                'scale': '6',
                'quantity_type': volume
            },
            {
                'name': 'Cup',
                'scale': '24',
                'quantity_type': volume
            },
            {
                'name': 'Pint',
                'scale': '48',
                'quantity_type': volume
            },
            {
                'name': 'Quart',
                'scale': '96',
                'quantity_type': volume
            },
            {
                'name': 'Gallon',
                'scale': '384',
                'quantity_type': volume
            }
        ]

        for quantity in quantities:
            Quantity.objects.create(**quantity)

    def test_00_create_recipe_fail(self):
        """
        Creating a recipe without a name should fail.
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
        response = client.post(reverse('recipes.views.create'), post_data)
        self.assertContains(response, 'This field is required', status_code=200)

    def test_01_create_and_get_recipe(self):
        """
        A recipe can be created and retrieved.
        :return:
        """
        client = Client()
        post_data = {
            'recipe-name': 'foo',
            'recipe-directions': 'bar',
            'ingredient_0-quantity_amount': '1 1/2',
            'ingredient_0-ingredient': 'flour',
            'ingredient_0-unit': 'cup',
            'ingredient_1-quantity_amount': '2',
            'ingredient_1-unit': 'count',
            'ingredient_1-ingredient': 'eggs'
        }
        response = client.post(
            reverse('recipes.views.create'),
            post_data,
            follow=True
        )
        self.assertRedirects(
            response,
            '/recipes/1',
            status_code=302,
            target_status_code=200,
            host=None,
            msg_prefix='',
            fetch_redirect_response=True
        )
        self.assertTrue(Recipe.objects.get(name='foo'))
        recipe = Recipe.objects.get(name='foo')
        self.assertEqual(len(recipe.recipe_ingredients), 2)
        eggs = RecipeIngredient.objects.get(
            recipe=recipe,
            ingredient=Ingredient.objects.get(name='eggs')
        )

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
