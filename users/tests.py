from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse

from users.models import CustomerUser


# Create your tests here.
class RegisterTestCase(TestCase):
    def test_user_create(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"mukhammad12",
                "first_name":"mukhammad",
                "last_name":'shamsidinov',
                "email":"mukhammad@gmail.com",
                "password":"somepassword"
            }
        )

        user = CustomerUser.objects.get(username="mukhammad12")

        self.assertEquals(user.username,"mukhammad12")
        self.assertEquals(user.first_name,'mukhammad')
        self.assertEquals(user.last_name,'shamsidinov')
        self.assertEquals(user.email,'mukhammad@gmail.com')
        self.assertNotEquals(user.password,'somepassword')
        self.assertTrue(user.check_password('somepassword'))


class LoginTestCase(TestCase):

    def test_login(self):
        user = CustomerUser.objects.create(username="admin",password="admin")
        user.set_password("admin")
        user.save()
        self.client.post(
            reverse("users:login"),
            data={
                "username":"admin",
                "password":"admin"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

