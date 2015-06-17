from django.test import TestCase
from ore.accounts.models import OreUser


class UsersTestCase(TestCase):

    def test_first_user_is_staff(self):

        user_john = OreUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')

        self.assertTrue(user_john.is_staff)
        self.assertTrue(user_john.is_superuser)

    def test_second_user_is_not_staff(self):
        user_john = OreUser.objects.create_user('john', 'password', 'john@ore.spongepowered.org')
        user_frank = OreUser.objects.create_user('frank', 'password', 'frank@ore.spongepowered.org')

        self.assertFalse(user_frank.is_staff)
        self.assertFalse(user_frank.is_superuser)
