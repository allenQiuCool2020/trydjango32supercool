from django.db import models
from django.contrib.auth.models import User
"""
- Global
    -Ingredients
    - Recipes
user
    -Recipes
        - Ingredients
        - Directions for ingredients
"""

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250) 
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE )
    name = models.CharField(max_length=250) 
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=250) # pounds, lbs
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)