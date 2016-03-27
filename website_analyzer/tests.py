"""testing module for website_analyzer app."""
import factory

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserFactory(factory.DjangoModelFactory):
    """generate user class using factory_boy."""
    class Meta:
        model = User

    username = 'test_user'
    password = 'temp_password'


class WebsiteAnalyzerDashboardTest(TestCase):
    """testing website_analyzer dashobard."""
    def setUp(self):
        user = UserFactory()
        user.set_password('test_password')
        user.save()
        self.client = Client()
        self.client.login(username=user.username, password='test_password')

    def test_get_dashboard_logged_in(self):
        'get dashboard for logged in user'
        response = self.client.get(
            reverse('website_analyzer:analyst_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website_analyzer/dashboard.html')

    def test_get_dashboard_not_logged_in(self):
        'get dashboard views without login, should be redirected to login page'
        user = UserFactory(username='bogus_user', password='another_user')
        bogus_client = Client()
        bogus_client.login(username=user.username, password='another_user')
        response = bogus_client.get(
            reverse('website_analyzer:analyst_dashboard'))
        self.assertRedirects(
            response,
            '{0}?next={1}'.format(
                reverse('login'),
                reverse('website_analyzer:analyst_dashboard')))
