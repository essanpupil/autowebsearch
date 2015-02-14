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
        resp = self.client.get('/website_management/')
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

    def test_webpage_does_not_exist(self):
        # test for web_id not exist in Webpage models
        web = Webpage.objects.all().values_list('id', flat=True)
        index = 1
        while index in web:
            index = index + 1
        resp = self.client.get('/website_management/webpage_detail/'
                                    + str(index) + '/')
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
        
class AddNewWebpageWebTest(WebTest):
    def test_insert_valid_url(self):
        form = self.app.get(reverse('website_management:add_new_webpage')).form
        form['url'] = 'http://sudutpandangpupil.blogspot.com/'
        response = form.submit().follow()
        self.assertIn(
            'http://sudutpandangpupil.blogspot.com/', response.content)
