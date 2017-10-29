from django.conf.urls import url, include
from django.contrib import admin
from .views import RecipesView, CreateRecipeView, RecipeView, UpdateRecipeView


urlpatterns = [
    url(r'^$', RecipesView.as_view(), name='recipes.views.recipes_view'),
    url(r'^(?P<pk>\d+)$', RecipeView.as_view(), name='recipes.views.recipe_view'),
    url(r'^(?P<pk>\d+)/edit/?$', UpdateRecipeView.as_view(), name='recipes.views.update'),
    url(r'^create/?$', CreateRecipeView.as_view(), name='recipes.views.create'),
]
