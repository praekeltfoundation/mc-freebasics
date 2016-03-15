import json
import pytest
import responses

from mc2.controllers.base.tests.base import ControllerBaseTestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from freebasics.models import FreeBasicsTemplateData, FreeBasicsController


@pytest.mark.django_db
class FreeBasicsControllerFormTestCase(TestCase, ControllerBaseTestCase):
    fixtures = ['test_users.json', 'test_social_auth.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.maxDiff = None
        self.client = Client()

    @responses.activate
    def test_template_create_and_delete_view(self):
        self.mock_create_marathon_app()

        self.client.login(username='testuser', password='test')
        post_data = {
            'site_name': 'example', 'site_name_url': 'example',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.post(reverse('template_list'), post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FreeBasicsTemplateData.objects.all().count(), 1)
        self.assertEqual(FreeBasicsController.objects.all().count(), 1)
        self.assertEqual(
            FreeBasicsController.objects.all().first().name,
            'example')
        self.assertEqual(
            FreeBasicsController.objects.all().first().domain_urls,
            'example.molo.site')
        pk = FreeBasicsTemplateData.objects.get(site_name='example').pk
        response = self.client.get(reverse(
            'template_detail', kwargs={'pk': pk}))
        self.assertEquals(response.data['site_name'], 'example')

        self.mock_update_marathon_app(
            FreeBasicsController.objects.all().first().app_id)

        post_data = {
            'site_name': 'example 2', 'site_name_url': 'example-2',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.put(reverse(
            'template_detail', kwargs={'pk': pk}), data=json.dumps(post_data),
            content_type='application/json')

        self.assertEquals(
            FreeBasicsTemplateData.objects.get(pk=pk).site_name, 'example 2')
        self.assertEquals(
            FreeBasicsTemplateData.objects.get(pk=pk).site_name_url,
            'example-2')
        self.assertEquals(
            FreeBasicsTemplateData.objects.get(pk=pk).controller.name,
            'example 2')
        self.assertEquals(
            FreeBasicsTemplateData.objects.get(pk=pk).controller.domain_urls,
            'example-2.molo.site')

        response = self.client.delete(reverse(
            'template_detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FreeBasicsTemplateData.objects.all().count(), 0)

    @responses.activate
    def test_marathon_app_data(self):
        self.mock_create_marathon_app()

        self.client.login(username='testuser', password='test')
        post_data = {
            'site_name': 'example', 'site_name_url': 'example',
            'base_background_color': 'purple',
            'block_background_color': 'teal',
            'body_font_family': 'helvetica', 'accent1': 'blue',
            'accent2': 'green', 'text_transform': 'uppercase',
            'block_font_family': 'arial'}
        response = self.client.post(reverse('template_list'), post_data)

        self.assertEqual(response.status_code, 201)

        controller = FreeBasicsController.objects.all().first()

        self.assertEquals(controller.get_marathon_app_data(), {
            "id": controller.app_id,
            "cpus": 0.1,
            "mem": 128.0,
            "instances": 1,
            "labels": {
                "domain": u"{}.{} {}".format(controller.app_id,
                                             settings.HUB_DOMAIN,
                                             'example.molo.site'),
                "name": u"example",
            },
            'env': {
                'BLOCK_POSITION_LATEST': '1',
                'BLOCK_POSITION_BANNER': '2',
                'BLOCK_POSITION_SECTIONS': '3',
                'BLOCK_POSITION_QUESTIONS': '4',
                'CUSTOM_CSS_ACCENT_1': u'blue',
                'CUSTOM_CSS_ACCENT_2': u'green',
                'CUSTOM_CSS_BASE_BACKGROUND_COLOR': u'purple',
                'CUSTOM_CSS_BODY_FONT_FAMILY': u'helvetica',
                'CUSTOM_CSS_BLOCK_BACKGROUND_COLOR': u'teal',
                'CUSTOM_CSS_BLOCK_FONT_FAMILY': u'arial',
                'CUSTOM_CSS_BLOCK_TEXT_TRANSFORM': u'uppercase',
                'CAS_SERVER_URL': 'http://testserver',
                'RAVEN_DSN': 'http://test-raven-dsn',
                'DATABASE_URL': 'sqlite:////path/to/media/molo.db',
            },
            "container": {
                "type": "DOCKER",
                "docker": {
                    "image": u"praekeltfoundation/molo-freebasics",
                    "forcePullImage": True,
                    "network": "BRIDGE",
                    "portMappings": [{"containerPort": 80, "hostPort": 0}],
                    "parameters": [
                        {"key": "volume-driver", "value": "xylem"},
                        {
                            "key": "volume",
                            "value":
                                "%s_media:/path/to/media/" % controller.app_id
                        }]
                }
            }
        })
