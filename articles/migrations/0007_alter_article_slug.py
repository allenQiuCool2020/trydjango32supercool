# Generated by Django 5.0.6 on 2024-06-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
