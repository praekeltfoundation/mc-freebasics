import json
import pytest
import responses

from mc2.controllers.base.tests.base import ControllerBaseTestCase
from mc2.organizations.models import Organization, OrganizationUserRelation

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
        self.mk_env_variable(controller)

        self.assertEquals(controller.get_marathon_app_data(), {
            "id": controller.app_id,
            "cpus": 0.1,
            "mem": 128.0,
            "instances": 1,
            "backoffFactor": 1.15,
            "backoffSeconds": 1,
            "labels": {
                "domain": u"{}.{} {}".format(controller.app_id,
                                             settings.HUB_DOMAIN,
                                             'example.molo.site'),
                "name": u"example",
                "traefik.frontend.rule":
                    u"Host: {}.test.com, {}".format(controller.app_id,
                                                    'example.molo.site'),
                'HAPROXY_GROUP': 'external',
                'HAPROXY_0_VHOST':
                    u'{}.test.com {}'.format(controller.app_id,
                                             'example.molo.site'),
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
                'SITE_NAME': u'example',
                u'TEST_KEY': u'a test value',
                'EMAIL_HOST': 'localhost',
                'EMAIL_PORT': 25,
                'EMAIL_HOST_USER': '',
                'EMAIL_HOST_PASSWORD': '',
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
            },
            "ports": [0],
            "healthChecks": [{
                "gracePeriodSeconds": 60,
                "intervalSeconds": 10,
                "maxConsecutiveFailures": 3,
                "path": u'/health/',
                "portIndex": 0,
                "protocol": "HTTP",
                "timeoutSeconds": 20
            }]
        })

    @responses.activate
    def test_use_postgres_db_if_provided(self):
        self.mock_create_marathon_app()

        self.client.login(username='testuser', password='test')
        post_data = {
            'site_name': 'example', 'site_name_url': 'example',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.post(reverse('template_list'), post_data)
        self.assertEqual(response.status_code, 201)

        controller = FreeBasicsController.objects.all().first()
        envs = controller.get_marathon_app_data()['env']
        self.assertEquals(
            envs['DATABASE_URL'],
            'sqlite:////path/to/media/molo.db')

        controller.postgres_db_url = 'postgres://user:pass@testserver/testdb'
        controller.save()

        envs = controller.get_marathon_app_data()['env']
        self.assertEquals(
            envs['DATABASE_URL'],
            'postgres://user:pass@testserver/testdb')

    def test_normal_user_with_no_org_has_permission_denied(self):
        self.client.login(username='testuser', password='test')
        response = self.client.get('/')
        self.assertContains(
            response,
            'You do not have permissions to use this site')

    def test_superuser_with_no_org_has_permission_to_add(self):
        User.objects.create_superuser('joe', 'joe@email.com', '1234')
        self.client.login(username='joe', password='1234')

        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver/add/')

    def test_superuser_sees_all_apps_if_they_exist(self):
        self.mock_create_marathon_app()
        self.client.login(username='testuser', password='test')
        post_data = {'site_name': 'Test App', 'site_name_url': 'test-app'}
        self.client.post(reverse('template_list'), post_data)

        self.client.logout()

        User.objects.create_superuser('joe', 'joe@email.com', '1234')
        self.client.login(username='joe', password='1234')

        response = self.client.get('/')
        self.assertContains(response, 'Test App')

    def test_normal_user_with_org_is_automatically_redirected_to_add(self):
        # normal user with org will see the Test App
        user = User.objects.create_user('joe', 'joe@email.com', '1234')
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(user=user, organization=org)

        self.client.login(username='joe', password='1234')

        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver/add/')
