from decimal import Decimal
import re
from django.forms import ModelForm, ValidationError, TextInput
from django.forms.widgets import  Textarea
from .models import RecipeIngredient, Recipe


class MaterializeModelForm(ModelForm):

    def materialize(self):
        """Returns this form rendered for materialize-css."""
        for name, field in self.fields.items():
            bf = self[name]
            if isinstance(bf.field.widget, Textarea):
                bf.field.widget.attrs['class']="materialize-textarea"

        return self._html_output(
            normal_row='<div class="input-field" %(html_class_attr)s>%(label)s %(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True
        )


class RecipeForm(MaterializeModelForm):

    prefix = 'recipe'

    class Meta:
        model = Recipe
        exclude = ['ingredients']

    def save(self):
        return super(RecipeForm, self).save()

    def is_valid(self):
        return super(RecipeForm, self).is_valid()


class RecipeIngredientForm(MaterializeModelForm):

    class Meta:
        model = RecipeIngredient
        exclude = []
        labels = {
            'quantity_amount': 'Qty'
        }
        widgets = {
            'ingredient': TextInput(attrs={'placeholder': 'Ingredient name'}),
            'quantity_amount': TextInput(
                attrs={
                    'placeholder': 'e.g. 1 1/4',
                    'size': 6,
                }),
        }

    def clean_quantity_amount(self):
        data = self.cleaned_data['quantity_amount']
        if not re.match(r'^([1-9]\d*)?\s?([1-9]\d*/[1-9]\d*)?$', data):
            raise ValidationError('Quantity is not a valid number or fraction.')
        return data

    def __init__(self, *args, **kwargs):
        """Override BaseModelForm init to set the ingredient value to the name of the ingredient rather than it's id."""
        instance = kwargs.get('instance')
        if instance is not None:
            initial = {
                'ingredient': str(getattr(instance, 'ingredient'))
            }
        else:
            initial = None
        super(RecipeIngredientForm, self).__init__(*args, initial=initial, **kwargs)
