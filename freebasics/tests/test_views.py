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

    def test_template_create_and_delete_view(self):
        self.client.login(username='testuser', password='test')
        post_data = {
            'site_name': 'example', 'site_name_url': 'https://example.com',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.post(reverse('template_detail'), post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FreeBasicsTemplateData.objects.all().count(), 1)
        self.assertEqual(FreeBasicsController.objects.all().count(), 1)
        pk = FreeBasicsTemplateData.objects.get(site_name='example').pk
        response = self.client.get(reverse(
            'template_detail', kwargs={'pk': pk}))
        self.assertEquals(response.data['site_name'], 'example')
        post_data = {
            'site_name': 'example2', 'site_name_url': 'https://example2.com',
            'body_background_color': 'purple', 'body_color': 'purple',
            'body_font_family': 'helvetica', 'accent1': '', 'accent2': ''}
        response = self.client.post(reverse(
            'template_detail', kwargs={'pk': pk}), post_data)
        self.assertEquals(
            FreeBasicsTemplateData.objects.get(pk=pk).site_name, 'example2')
        response = self.client.delete(reverse(
            'template_detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FreeBasicsTemplateData.objects.all().count(), 0)
