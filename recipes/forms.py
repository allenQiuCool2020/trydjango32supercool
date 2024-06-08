from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(help_text='This is your help')
    # desciption = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "placeholder": f"Recipe {str(field)}",
                "class": "form-control"
            }
        
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # self.fields['name'].widget.attrs.update({'class':'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows':'2'})
        self.fields['directions'].widget.attrs.update({'rows':'4'})

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']