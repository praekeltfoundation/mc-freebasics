import pytest
from mc2.controllers.base.tests.base import ControllerBaseTestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from freebasics.models import FreeBasicsTemplateData, FreeBasicsController


@pytest.mark.django_db
class FreeBasicsControllerFormTestCase(TestCase, ControllerBaseTestCase):
    fixtures = ['test_users.json', 'test_social_auth.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.maxDiff = None
        self.client = Client()

    def test_template_list_post_view(self):
        self.client.login(username='testuser', password='test')
        post_data = {
            'site_name': 'example', 'site_name_url': 'https://example.com',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.post(reverse('templates_list'), post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FreeBasicsTemplateData.objects.all().count(), 1)
        self.assertEqual(FreeBasicsController.objects.all().count(), 1)
