"""testing module for administrative app."""
import factory

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserFactory(factory.DjangoModelFactory):
    """generate user for test using factory."""
    class Meta:
        model = User

    username = 'test_user'
    password = 'temp_password'


class UserTest(TestCase):
    """testing user operations."""
    def setUp(self):
        test_user = UserFactory()
        test_user.set_password('test_password')
        test_user.is_staff = True
        test_user.save()
        self.client = Client()
        self.client.login(
            username=test_user.username, password='test_password')

    def test_dashboard_administrative(self):
        "requesting administrative dashboard views."
        response = self.client.get(reverse('administrative:admin_dashboard'))
        self.assertEqual(response.status_code, 200, response.templates)
        self.assertTemplateUsed(response, 'administrative/dashboard.html')
