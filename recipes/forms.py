from decimal import Decimal
import re
from django.forms import ModelForm, ValidationError
from .models import RecipeIngredient, Recipe


class RecipeForm(ModelForm):

    prefix = 'recipe'

    class Meta:
        model = Recipe
        exclude = ['ingredients']

    def save(self):
        return super(RecipeForm, self).save()

    def is_valid(self):
        return super(RecipeForm, self).is_valid()


class RecipeIngredientForm(ModelForm):

    class Meta:
        model = RecipeIngredient
        exclude = []
        labels = {
            'name': 'Name',
            'quantity_amount': 'Qty'
        }

    def clean_quantity_amount(self):
        data = self.cleaned_data['quantity_amount']
        if not re.match(r'^([1-9]\d*)?\s?([1-9]\d*/[1-9]\d*)?$', data):
            raise ValidationError('Quantity is not a valid number or fraction.')
        return data