import pytest
from mc2.controllers.base.tests.base import ControllerBaseTestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


@pytest.mark.django_db
class FreeBasicsControllerFormTestCase(TestCase, ControllerBaseTestCase):
    fixtures = ['test_users.json', 'test_social_auth.json']

    def setUp(self):
        self.user = User.objects.create(username='tester', password='tester')
        self.maxDiff = None

    def test_template_list_post_view(self):
        client = Client()
        client.login(username='tester', password='tester')
        response = client.get('/')
        post_data = {
            'site_name': 'example', 'site_name_url': 'https://example.com',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = client.post(reverse('templates_list'), post_data)
        print response
        self.assertContains(response, 'position')
