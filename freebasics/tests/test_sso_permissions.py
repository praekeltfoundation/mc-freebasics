import pytest

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from freebasics import permissions
from freebasics.models import FreeBasicsController

from mc2.controllers.base.tests.base import ControllerBaseTestCase
from mc2.organizations.models import Organization, OrganizationUserRelation


@pytest.mark.django_db
class SSOTestCase(TestCase, ControllerBaseTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@email.com', '1234')
        self.client = Client()

    def test_group_access(self):
        user = User.objects.create(first_name='foo')
        attr = permissions.org_permissions(user, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

    def test_user_details(self):
        user = User.objects.create(first_name='foo', email='foo@email.com')
        attr = permissions.org_permissions(user, 'http://foobar.com/')
        self.assertEqual(attr['givenName'], 'foo')
        self.assertEqual(attr['email'], 'foo@email.com')

    def test_org_admin_must_have_superuser_access(self):
        user = User.objects.create_user('joe', 'joe@email.com', '1234')
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(
            user=user, organization=org, is_admin=True)

        self.client.login(username='joe', password='1234')
        post_data = {'site_name': 'Test App', 'site_name_url': 'test-app'}
        self.client.post(reverse('template_list'), post_data)

        attr = permissions.org_permissions(user, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

        attr = permissions.org_permissions(user, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], True)

    def test_super_user_must_have_super_user_acess(self):
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(
            user=self.user, organization=org, is_admin=True)

        joe = User.objects.create_superuser('joe', 'joe@email.com', '1234')
        self.client.login(username='joe', password='1234')
        post_data = {'site_name': 'Test App', 'site_name_url': 'test-app'}
        self.client.post(reverse('template_list'), post_data)

        attr = permissions.org_permissions(joe, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], True)

        attr = permissions.org_permissions(joe, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], True)

    def test_user_in_org_must_have_access(self):
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(
            user=self.user, organization=org, is_admin=True)

        # joe is a normal user in the org (is_admin = False)
        joe = User.objects.create_user('joe', 'joe@email.com', '1234')
        OrganizationUserRelation.objects.create(
            user=joe, organization=org)

        # create the controller as testuser
        self.client.login(username='testuser', password='1234')
        post_data = {'site_name': 'Test App', 'site_name_url': 'test-app'}
        self.client.post(reverse('template_list'), post_data)

        attr = permissions.org_permissions(joe, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

        attr = permissions.org_permissions(joe, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], False)

    def test_user_in_other_org_must_not_have_cross_access(self):
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(
            user=self.user, organization=org, is_admin=True)

        # joe is a normal user in the org (is_admin = False)
        joe = User.objects.create_user('joe', 'joe@email.com', '1234')
        OrganizationUserRelation.objects.create(
            user=joe, organization=org)

        # sam is a normal user in other org
        sam = User.objects.create_user('sam', 'sam@email.com', '1234')
        other_org = Organization.objects.create(name='Other', slug='other')
        OrganizationUserRelation.objects.create(
            user=sam, organization=other_org)

        attr = permissions.org_permissions(sam, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

        attr = permissions.org_permissions(sam, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

        # tom is an admin user in other org
        tom = User.objects.create_user('tom', 'tom@email.com', '1234')
        other_org = Organization.objects.create(name='Other', slug='other')
        OrganizationUserRelation.objects.create(
            user=tom, organization=other_org)

        attr = permissions.org_permissions(tom, 'http://foobar.com/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

        attr = permissions.org_permissions(tom, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], False)
        self.assertEqual(attr['is_admin'], False)

    def test_access_using_generic_domain(self):
        user = User.objects.create_user('joe', 'joe@email.com', '1234')
        org = Organization.objects.create(name='Test', slug='test')
        OrganizationUserRelation.objects.create(
            user=user, organization=org, is_admin=True)

        self.client.login(username='joe', password='1234')
        post_data = {'site_name': 'Test App', 'site_name_url': 'test-app'}
        self.client.post(reverse('template_list'), post_data)

        attr = permissions.org_permissions(user, 'http://test-app.molo.site/')
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], True)

        controller = FreeBasicsController.objects.all().first()

        attr = permissions.org_permissions(
            user, 'http://%s.test.com/admin/' % controller.app_id)
        self.assertEqual(attr['has_perm'], True)
        self.assertEqual(attr['is_admin'], True)
