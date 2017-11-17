from decimal import Decimal
import copy
import re
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Ingredient, Recipe
from .forms import RecipeIngredientForm, RecipeForm


class RecipesView(ListView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super(RecipesView, self).get_context_data(**kwargs)
        return context


class CreateRecipeView(CreateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, *args, **kwargs):
        context = super(CreateRecipeView, self).get_context_data(*args, **kwargs)
        context['ingredient_item'] = RecipeIngredientForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Process Post requests for creating recipes.

        :param request: WSGCI request object.
        :return: rendered HTTP response
        """

        # Get HTTP response from processing the form in self.form_class
        response = super(CreateRecipeView, self).post(self, request, *args, **kwargs)

        # If a response of 200 is returned, then the form failed and isn't redirecting to a new
        # recipe.
        if response.status_code == 200:
            return response

        # Get a list of recipe ingredient form prefixes.
        ingrdient_form_prefixes = list(set(
            re.sub(r'-.+', '', key) for key in request.POST if re.match(r'^ingredient_\d+-', key)
        ))

        # Create a list to store new recipe ingredients in.
        recipe_ingredient_forms = list()

        # Create a duplicate of the post data so that it can be modified in order to set the recipe
        # for each ingredient.
        data = copy.deepcopy(request.POST)

        for prefix in ingrdient_form_prefixes:
            # Set the recipe that owns this ingredient.
            data[prefix + '-recipe'] = self.get_form().instance.id

            # Find or create the ingredient from the ingredient table.
            data[prefix + '-ingredient'] = Ingredient.objects.get_or_create(
                name=data[prefix + '-ingredient']
            )[0].id

            # Instantiate a form with the provided data and append it to the list of recipe
            # ingreients.
            recipe_ingredient_forms.append(RecipeIngredientForm(data=data, prefix=prefix))

            # Ensure the ingredient form is valid.
            if recipe_ingredient_forms[-1].is_valid():
                recipe_ingredient_forms[-1].save()

        # build additional context

        return response


class RecipeView(DetailView):
    model = Recipe

    #def get(self):
    #    super().get()

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeView, self).get_context_data(*args, **kwargs)
        context['recipe_ingredients'] = list(self.object.recipe_ingredients)
        return context


class UpdateRecipeView(UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateRecipeView, self).get_context_data(*args, **kwargs)
        context['ingredient_item'] = RecipeIngredientForm()
        from pprint import pprint
        context['ingredients'] = list(
            RecipeIngredientForm(instance=recipe_ingredient)
            for recipe_ingredient in self.object.recipe_ingredients
            )
        #pprint(context['ingredient_item'].__dict__)
        return context

    def post(self, request, *args, **kwargs):
        return super(UpdateRecipeView, self).post(self, request, *args, **kwargs)
