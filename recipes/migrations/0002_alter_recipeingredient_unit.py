# Generated by Django 5.0.6 on 2024-06-07 08:17

import recipes.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(max_length=250, validators=[recipes.validators.validate_unit_of_measure]),
        ),
    ]
