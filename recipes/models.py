from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=30)
    directions = models.TextField()
    prep_time = models.DurationField(blank=True, null=True)
    cook_time = models.DurationField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    def get_absolute_url(self):
        return reverse('recipes.views.recipe_view', args=[str(self.id)])

    @property
    def recipe_ingredients(self):
        return RecipeIngredient.objects.filter(recipe=self)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    quantity_amount = models.TextField(max_length=8)

    @property
    def name(self):
        return self.ingredient.name
