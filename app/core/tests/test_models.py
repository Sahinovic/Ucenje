from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email = 'test@test.com', password = 'testpass'):
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_succ(self):

        email = 'mirza@gmail.com'
        password = 'testtest'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        email = 'mirza@MIRZA.COM'
        user = get_user_model().objects.create_user(email, 'testtest')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None , '1234')


    def test_super_user_is_created(self):
        user = get_user_model().objects.create_superuser('mirza@gmail.com', "test1234")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user = sample_user(),
            name='vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingedients_str(self):
        ingredient= models.Ingredient.objects.create(
            user = sample_user(),
            name='kupus'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='sos u gljivama',
            time_minutes=5,
            price= 5.00
        )

        self.assertEqual(str(recipe), recipe.title)