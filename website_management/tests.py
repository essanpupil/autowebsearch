import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from website_management.models import Webpage, Homepage, Domain


class WebsiteDashboardViewsTestCase(TestCase):
    "Testing dashboard views"
    def setUp(self):
        Webpage.objects.create(url="http://www.pupil.com/profil/")
        Webpage.objects.create(url="http://www.facebok.com/essanpupil/")
        Webpage.objects.create(url="http://www.detik.com/sepakbola/")
        Webpage.objects.create(url="http://www.kompas.com/news/")
        Webpage.objects.create(url="http://www.twiter.com/setting/")
        Webpage.objects.create(url="http://www.republika.co.id/islam/")
        Domain.objects.create(name="pupil.com")
        Domain.objects.create(name="kompas.com")
        Domain.objects.create(name="facebok.com")
        Domain.objects.create(name="detik.com")
        Domain.objects.create(name="twiter.com")
        Domain.objects.create(name="republika.co.id")
        Homepage.objects.create(name="www.pupil.com")
        Homepage.objects.create(name="www.facebok.com")
        Homepage.objects.create(name="www.detik.com")
        Homepage.objects.create(name="www.kompas.com")
        Homepage.objects.create(name="www.twiter.com")
        Homepage.objects.create(name="www.republika.co.id")
        webpage = Webpage.objects.get(url="http://www.pupil.com/profil/")
        domain = Domain.objects.get(name="pupil.com")
        homepage = Homepage.objects.get(name="www.pupil.com")
        homepage.domain = domain
        homepage.save()
        webpage.homepage = homepage
        webpage.save()

    def test_filled_website_dashboard(self):
        resp = self.client.get(reverse('website_management:website_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('web_count' in resp.context)
        self.assertTrue('hp_count' in resp.context)
        self.assertTrue('dom_count' in resp.context)
        self.assertTrue('newest_5_web' in resp.context)
        self.assertTrue('newest_5_dom' in resp.context)
        self.assertTrue('newest_5_hp' in resp.context)
        self.assertEqual(resp.context['web_count'], 6)
        self.assertEqual(resp.context['hp_count'], 6)
        self.assertEqual(resp.context['dom_count'], 6)

    def test_filled_website_dashboard_html_render(self):
        resp = self.client.get(reverse('website_management:website_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp,
                            'http://www.facebok.com/essanpupil/', 1)
        self.assertContains(resp,
                            'http://www.detik.com/sepakbola/', 1)
        self.assertContains(resp,
                            'http://www.kompas.com/news/', 1)
        self.assertContains(resp,
                            'http://www.twiter.com/setting/', 1)
        self.assertContains(resp,
                            'http://www.republika.co.id/islam/', 1)
        self.assertContains(resp, 'facebok.com', 3)
        self.assertContains(resp, 'detik.com', 3)
        self.assertContains(resp, 'kompas.com', 3)
        self.assertContains(resp, 'twiter.com', 3)
        self.assertContains(resp, 'republika.co.id', 3)
        self.assertNotContains(resp, 'www.pupil.com')
        self.assertNotContains(resp, 'http://www.pupil.com/profil/')
        self.assertNotContains(resp, 'blogspot.com')


class WebpageDetailViewsTestcase(TestCase):
    def setUp(self):
        domain = Domain.objects.create(name="pupil.com")
        homepage = Homepage.objects.create(name="www.pupil.com", domain=domain)
        Webpage.objects.create(url="http://www.pupil.com/profil/",
                               homepage=homepage)

    def test_webpage_does_not_exist(self):
        # test for web_id not exist in Webpage models
        web = Webpage.objects.all().values_list('id', flat=True)
        index = 1
        while index in web:
            index += 1
        resp = self.client.get(
            reverse('website_management:webpage_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_webpage_detail_from_setup_data(self):
        # test web detail based-on setup() above
        web = Webpage.objects.get(url="http://www.pupil.com/profil/")
        url_test = reverse('website_management:webpage_detail',
                           kwargs={'web_id': web.id})
        resp = self.client.get(url_test)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(web.url, resp.content)
        self.assertIn(str(int(web.id)), resp.content)
        self.assertIn(str(int(web.homepage.id)), resp.content)
        self.assertIn(str(int(web.homepage.domain.id)), resp.content)
        self.assertIn(web.homepage.name, resp.content)
        self.assertIn(web.homepage.domain.name, resp.content)


class HomepageDetailViewsTestcase(TestCase):
    def setUp(self):
        domain = Domain.objects.create(name="pupil.com")
        Homepage.objects.create(name="www.pupil.com", domain=domain)

    def test_homepage_does_not_exist(self):
        # test for web_id not exist in Webpage models
        homepage = Homepage.objects.all().values_list('id', flat=True)
        index = 1
        while index in homepage:
            index += 1
        resp = self.client.get(
            reverse('website_management:homepage_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_homepage_detail_from_setup_data(self):
        # test web detail based-on setup() above
        homepage = Homepage.objects.get(name="www.pupil.com")
        url_test = reverse('website_management:homepage_detail',
                           kwargs={'hp_id': homepage.id})
        resp = self.client.get(url_test)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('pupil.com', str(homepage.domain.name))
        self.assertIn(homepage.name, resp.content)
        self.assertIn(str(int(homepage.id)), resp.content)
        self.assertIn(str(int(homepage.domain.id)), resp.content)


class DomainDetailViewsTestcase(TestCase):
    def setUp(self):
        Domain.objects.create(name="pupil.com")

    def test_domain_does_not_exist(self):
        # test for web_id not exist in Webpage models
        domain = Domain.objects.all().values_list('id', flat=True)
        index = 1
        while index in domain:
            index += 1
        resp = self.client.get(
            reverse('website_management:domain_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_domain_detail_from_setup_data(self):
        # test web detail based-on setup() above
        domain = Domain.objects.get(name="pupil.com")
        url_test = reverse('website_management:domain_detail',
                           kwargs={'dom_id': domain.id})
        resp = self.client.get(url_test)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(domain.name, resp.content)
        self.assertIn(str(int(domain.id)), resp.content)


class AddNewWebpageWebTest(WebTest):
    def test_insert_valid_url(self):
        form = self.app.get(reverse('website_management:add_new_webpage')).form
        form['url'] = 'http://sudutpandangpupil.blogspot.com/'
        response = form.submit().follow()
        self.assertIn('http://sudutpandangpupil.blogspot.com/',
                      response.content)


class ViewAllWebpagesTestCase(TestCase):
    def setUp(self):
        Webpage.objects.create(url="http://www.pupil.com/profil/")
        Webpage.objects.create(url="http://www.facebook.com/essanpupil/")
        Webpage.objects.create(url="http://www.detik.com/sepakbola/")
        Webpage.objects.create(url="http://www.kompas.com/news/")
        Webpage.objects.create(url="http://www.twitter.com/setting/")
        Webpage.objects.create(url="http://www.republika.co.id/islam/")

    def test_view_all_webpages_(self):
        resp = self.client.get(reverse('website_management:view_all_webpages'))
        self.assertIn("http://www.pupil.com/profil/", resp.content)
        self.assertIn("http://www.facebook.com/essanpupil/", resp.content)
        self.assertIn("http://www.detik.com/sepakbola/", resp.content)
        self.assertIn("http://www.kompas.com/news/", resp.content)
        self.assertIn("http://www.twitter.com/setting/", resp.content)
        self.assertIn("http://www.republika.co.id/islam/", resp.content)
        self.assertTrue(resp.status_code, 200)
        self.assertIn('webs', resp.context.keys())
        self.assertTrue(len(resp.context['webs']),
                        Webpage.objects.all().count())
        self.assertEqual(resp.context['webs'][0].keys().sort(),
                         ['url', 'date_added', 'last_response',
                          'last_response_check', 'id'].sort())


class ViewAllHomepagesTestCase(TestCase):
    def setUp(self):
        domain = Domain.objects.create(name="pupil.com")
        Homepage.objects.create(name="www.pupil.com", domain=domain)
        domain = Domain.objects.create(name="facebook.com")
        Homepage.objects.create(name="www.facebook.com", domain=domain)
        domain = Domain.objects.create(name="detik.com")
        Homepage.objects.create(name="www.detik.com", domain=domain)
        domain = Domain.objects.create(name="kompas.com")
        Homepage.objects.create(name="www.kompas.com", domain=domain)
        domain = Domain.objects.create(name="twitter.com")
        Homepage.objects.create(name="www.twitter.com", domain=domain)
        domain = Domain.objects.create(name="republika.co.id")
        Homepage.objects.create(name="www.republika.co.id", domain=domain)

    def test_view_all_homepages_(self):
        resp = self.client.get(
            reverse('website_management:view_all_homepages'))
        self.assertIn("www.pupil.com", resp.content)
        self.assertIn("www.facebook.com", resp.content)
        self.assertIn("www.detik.com", resp.content)
        self.assertIn("www.kompas.com", resp.content)
        self.assertIn("www.twitter.com", resp.content)
        self.assertIn("www.republika.co.id", resp.content)
        self.assertTrue(resp.status_code, 200)
        self.assertIn('homes', resp.context.keys())
        self.assertTrue(len(resp.context['homes']),
                        Homepage.objects.all().count())
        self.assertEqual(resp.context['homes'][0].keys().sort(),
                         ['name', 'date_added', 'domain', 'id'].sort())


class ViewAllDomainsTestCase(TestCase):
    def setUp(self):
        Domain.objects.create(name="pupil.com")
        Domain.objects.create(name="facebook.com")
        Domain.objects.create(name="detik.com")
        Domain.objects.create(name="kompas.com")
        Domain.objects.create(name="twitter.com")
        Domain.objects.create(name="republika.co.id")

    def test_view_all_homepages_(self):
        resp = self.client.get(reverse('website_management:view_all_domains'))
        now = datetime.datetime.now()
        self.assertIn("pupil.com", resp.content)
        self.assertIn("facebook.com", resp.content)
        self.assertIn("detik.com", resp.content)
        self.assertIn("kompas.com", resp.content)
        self.assertIn("twitter.com", resp.content)
        self.assertIn("republika.co.id", resp.content)
        self.assertTrue(resp.status_code, 200)
        self.assertIn('doms', resp.context.keys())
        self.assertTrue(len(resp.context['doms']),
                        Homepage.objects.all().count())
        self.assertIn('name', resp.context['doms'][0].keys())
        self.assertIn('date_added', resp.context['doms'][0].keys())
        self.assertIn('id', resp.context['doms'][0].keys())
        self.assertEqual(resp.context['doms'][0]['date_added'], now.date())


class SearchWebpagesTestCase(WebTest):
    def online_search_webpage(self):
        """
        This test method is NOT meant tobe run on project test. You should run
        this one specific method test. when the keyword is queried to google,
        the result in 1 page will be save to database. this method search
        url that contain the keyword, which means, if exist, the search is
        success and saved.
        """
        form = self.app.get(reverse('website_management:search_webpage')).form
        form['keyword'] = 'essanpupil'
        form['page'] = '1'
        form.submit().follow()
        webs = Webpage.objects.filter(url__contains='essanpupil')
        self.assertEqual(bool(webs.count()), True)
