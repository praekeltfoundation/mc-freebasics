import pytest
from mc2.controllers.base.tests.base import ControllerBaseTestCase
from mc2.organizations.models import Organization

from freebasics.forms import FreeBasicsControllerForm
from freebasics.models import FreeBasicsController

from django.contrib.auth.models import User
from django.http import QueryDict


@pytest.mark.django_db
class FreeBasicsControllerFormTestCase(ControllerBaseTestCase):
    fixtures = [
        'test_users.json', 'test_social_auth.json', 'test_organizations.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.maxDiff = None

    def test__process_data_empty(self):
        form = FreeBasicsControllerForm()
        self.assertIsNone(form._process_data(None))

    def test__process_data(self):
        data = QueryDict(mutable=True)
        data.appendlist('name', 'Test App')
        data.appendlist('selected_template', 'option1')
        form = FreeBasicsControllerForm()
        self.assertIsNotNone(form._process_data(data))

    def test__process_data_error(self):
        data = QueryDict(mutable=True)
        data.appendlist('name', 'Test App')
        data.appendlist('selected_template', 'optio')
        form = FreeBasicsControllerForm()
        self.assertRaises(KeyError, form._process_data, data)

    def test__get_docker_image_name(self):
        for t in FreeBasicsController.TEMPLATE_CHOICES:
            controller = FreeBasicsController.objects.create(
                name='Test App',
                owner=self.user,
                selected_template=t[0],
            )
            controller.save()
            form = FreeBasicsControllerForm(instance=controller)
            self.assertEqual(form._get_docker_image_name(t[0]),
                             "universalcore/" +
                             dict(FreeBasicsController.TEMPLATE_CHOICES)[t[0]])

    def test__get_marathon_cmd(self):
        for t in FreeBasicsController.TEMPLATE_CHOICES:
            controller = FreeBasicsController.objects.create(
                name='Test App',
                owner=self.user,
                selected_template=t[0],
            )
            controller.save()
            form = FreeBasicsControllerForm(instance=controller)
            self.assertRegexpMatches(
                form._get_marathon_cmd(t[0]),
                "./deploy/docker-entrypoint.sh [A-Za-z]+ [A-Za-z]+\.wsgi 8000")

    def test__freebasics_app_id_prefix(self):
        for t in FreeBasicsController.TEMPLATE_CHOICES:
            controller = FreeBasicsController.objects.create(
                name='Test App',
                owner=self.user,
                selected_template=t[0],
            )
            self.assertTrue(controller.app_id.startswith('freebasics-'))

    def test__homepage_redirects_to_create_page_if_no_app_yet(self):
        self.client.login(username='testuser', password='test')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/add/')

    def test__homepage_shows_correct_app(self):
        self.client.login(username='testuser', password='test')

        controller = FreeBasicsController.objects.create(
            name='Happy Place',
            owner=self.user,
            selected_template=FreeBasicsController.TEMPLATE_CHOICES[0],
        )
        controller.organization = Organization.objects.get(pk=1)
        controller.save()

        response = self.client.get('/')
        self.assertContains(response, 'Happy Place')
