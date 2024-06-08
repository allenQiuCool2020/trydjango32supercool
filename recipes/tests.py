from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredient
from django.core.exceptions import ValidationError
# Create your tests here.

User = get_user_model()

# class UserTestCase(TestCase):
#     def setUp(self):
#         self.user_a = User.objects.create_user('cfe', password="123")
#     def test_user_pw(self):
#         checked = self.user_a.check_password("123")
#         self.assertTrue(checked)

class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe', password="abc!123")
        self.recipe_a = Recipe.objects.create(
            name='grilled chicken',
            user = self.user_a,
        )
        self.recipe_b = Recipe.objects.create(
            name='grilled chickenaa',
            user = self.user_a,
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe = self.recipe_a,
            name = "chicken",
            quantity = "1/2",
            unit = "pound"
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe = self.recipe_a,
            name = "chicken",
            quantity = "1/2aaa",
            unit = "pound"
        )

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(),1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        print(qs)
        self.assertEqual(qs.count(),2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(),2)

    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()

        self.assertEqual(qs.count(),2)

    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(),2)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(),2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id",flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        print(qs)
        self.assertEqual(qs.count(),2)

    def test_unit_measure_validation_error(self):
        invalid_unit = "aaaadfsd"
        with self.assertRaises(ValidationError):
            ingredient = RecipeIngredient(
                name = "new",
                quantity = 10,
                recipe = self.recipe_a,
                unit = invalid_unit
            )
            ingredient.full_clean ()

    def test_unit_measure_validation(self):
        invalid_unit = "kilograms"
        ingredient = RecipeIngredient(
            name = "new",
            quantity = 10,
            recipe = self.recipe_a,
            unit = invalid_unit
        )
        ingredient.full_clean ()

    def test_qty_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)

