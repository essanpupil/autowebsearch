from django.test import TestCase


class AdministrativeDashboardTestCase(TestCase):
    def test_view_admin_dashboard(self):
        "Display admin dashboard view"
        selt.client.login(username=user.username, password=
        resp = self.client.get(reverse('administrative:view_dashboard'))
        self.assertEqual(resp.status_code, 200)
