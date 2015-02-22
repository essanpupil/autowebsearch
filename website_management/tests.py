from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.db import IntegrityError

from .models import Webpage, Homepage, Domain
from .forms import AddWebpageForm


class WebsiteDashboardViewsTestCase(TestCase):
    def setUp(self):
        Webpage.objects.create(url="http://www.pupil.com/profil/")
        Webpage.objects.create(url="http://www.facebook.com/essanpupil/")
        Webpage.objects.create(url="http://www.detik.com/sepakbola/")
        Webpage.objects.create(url="http://www.kompas.com/news/")
        Webpage.objects.create(url="http://www.twitter.com/setting/")
        Webpage.objects.create(url="http://www.republika.co.id/islam/")
        Domain.objects.create(name="pupil.com")
        Domain.objects.create(name="blogspot.com")
        Domain.objects.create(name="facebook.com")
        Domain.objects.create(name="detik.com")
        Domain.objects.create(name="twitter.com")
        Domain.objects.create(name="republika.co.id")
        Homepage.objects.create(name="www.pupil.com")
        Homepage.objects.create(name="www.facebook.com")
        Homepage.objects.create(name="www.detik.com")
        Homepage.objects.create(name="www.kompas.com")
        Homepage.objects.create(name="www.twitter.com")
        Homepage.objects.create(name="www.republika.co.id")
        web = Webpage.objects.get(url="http://www.pupil.com/profil/")
        dom = Domain.objects.get(name="pupil.com")
        hp = Homepage.objects.get(name="www.pupil.com")
        hp.domain = dom
        hp.save()
        web.homepage = hp
        web.save()

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
        self.assertIn("http://www.facebook.com/essanpupil/", resp.content)
        self.assertIn("http://www.detik.com/sepakbola/", resp.content)
        self.assertIn("http://www.kompas.com/news/", resp.content)
        self.assertIn("http://www.twitter.com/setting/", resp.content)
        self.assertIn("http://www.republika.co.id/islam/", resp.content)
        self.assertFalse(
            "www.pupil.com" in resp.context['newest_5_hp'][0].values())
        self.assertFalse("http://www.pupil.com/profil/" in
                            resp.context['newest_5_web'][0].values())
        self.assertFalse(
            "blogspot.com" in resp.context['newest_5_dom'][0].values())

class WebpageDetailViewsTestcase(TestCase):
    def setUp(self):
        dom = Domain.objects.create(name="pupil.com")
        hp = Homepage.objects.create(name="www.pupil.com", domain=dom)
        web = Webpage.objects.create(url="http://www.pupil.com/profil/",
                                        homepage=hp)
        

    def test_webpage_does_not_exist(self):
        # test for web_id not exist in Webpage models
        web = Webpage.objects.all().values_list('id', flat=True)
        index = 1
        while index in web:
            index = index + 1
        resp = self.client.get(
                reverse('website_management:webpage_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_webpage_detail_from_setup_data(self):
        # test web detail based-on setup() above
        web = Webpage.objects.get(url="http://www.pupil.com/profil/")
        url_test = reverse('website_management:webpage_detail',
                                kwargs={'web_id':web.id})
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
        dom = Domain.objects.create(name="pupil.com")
        hp = Homepage.objects.create(name="www.pupil.com", domain=dom)

    def test_homepage_does_not_exist(self):
        # test for web_id not exist in Webpage models
        hp = Homepage.objects.all().values_list('id', flat=True)
        index = 1
        while index in hp:
            index = index + 1
        resp = self.client.get(
                reverse('website_management:homepage_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_homepage_detail_from_setup_data(self):
        # test web detail based-on setup() above
        hp = Homepage.objects.get(name="www.pupil.com")
        url_test = reverse('website_management:homepage_detail',
                                kwargs={'hp_id': hp.id})
        resp = self.client.get(url_test)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('pupil.com', str(hp.domain.name))
        self.assertIn(hp.name, resp.content)
        self.assertIn(str(int(hp.id)), resp.content)
        self.assertIn(str(int(hp.domain.id)), resp.content)
        
class DomainDetailViewsTestcase(TestCase):
    def setUp(self):
        dom = Domain.objects.create(name="pupil.com")        

    def test_domain_does_not_exist(self):
        # test for web_id not exist in Webpage models
        dom = Domain.objects.all().values_list('id', flat=True)
        index = 1
        while index in dom:
            index = index + 1
        resp = self.client.get(
                reverse('website_management:domain_detail', args=[index]))
        self.assertEqual(resp.status_code, 404)

    def test_domain_detail_from_setup_data(self):
        # test web detail based-on setup() above
        dom = Domain.objects.get(name="pupil.com")
        url_test = reverse('website_management:domain_detail',
                                kwargs={'dom_id': dom.id})
        resp = self.client.get(url_test)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(dom.name, resp.content)
        self.assertIn(str(int(dom.id)), resp.content)
        
class AddNewWebpageWebTest(WebTest):
    def test_insert_valid_url(self):
        form = self.app.get(reverse('website_management:add_new_webpage')).form
        form['url'] = 'http://sudutpandangpupil.blogspot.com/'
        response = form.submit().follow()
        self.assertIn(
            'http://sudutpandangpupil.blogspot.com/', response.content)

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
        dom = Domain.objects.create(name="pupil.com")
        Homepage.objects.create(name="www.pupil.com", domain=dom)
        dom = Domain.objects.create(name="facebook.com")
        Homepage.objects.create(name="www.facebook.com", domain=dom)
        dom = Domain.objects.create(name="detik.com")
        Homepage.objects.create(name="www.detik.com", domain=dom)
        dom = Domain.objects.create(name="kompas.com")
        Homepage.objects.create(name="www.kompas.com", domain=dom)
        dom = Domain.objects.create(name="twitter.com")
        Homepage.objects.create(name="www.twitter.com", domain=dom)
        dom = Domain.objects.create(name="republika.co.id")
        Homepage.objects.create(name="www.republika.co.id", domain=dom)

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
        dom = Domain.objects.create(name="pupil.com")
        dom = Domain.objects.create(name="facebook.com")
        dom = Domain.objects.create(name="detik.com")
        dom = Domain.objects.create(name="kompas.com")
        dom = Domain.objects.create(name="twitter.com")
        dom = Domain.objects.create(name="republika.co.id")

    def test_view_all_homepages_(self):
        resp = self.client.get(
                    reverse('website_management:view_all_domains'))
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
        self.assertEqual(resp.context['doms'][0].keys().sort(),
                            ['name', 'date_added', 'id'].sort())

