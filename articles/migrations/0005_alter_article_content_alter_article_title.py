# Generated by Django 5.0.6 on 2024-06-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
