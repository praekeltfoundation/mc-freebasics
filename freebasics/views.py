from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings

from mc2.controllers.base.views import ControllerCreateView, ControllerEditView
from mc2.views import HomepageView
from mc2.organizations.models import Organization
from mc2.organizations.utils import active_organization
from mc2 import tasks

from freebasics.models import FreeBasicsTemplateData, FreeBasicsController
from freebasics.serializers import FreeBasicsDataSerializer
from freebasics.tasks import update_marathon_app
from rest_framework import generics


class TemplateDataCreate(generics.ListCreateAPIView):
    queryset = FreeBasicsTemplateData.objects.all()
    serializer_class = FreeBasicsDataSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        controller = FreeBasicsController.objects.create(
            owner=self.request.user,
            organization=active_organization(self.request),
            docker_image=settings.FREE_BASICS_DOCKER_IMAGE,
            volume_path=settings.FREE_BASICS_VOLUME_PATH,
            volume_needed=True,
            port=settings.FREE_BASICS_DOCKER_PORT,
            name=data.get('site_name'),
            domain_urls='%s.%s' % (
                data.get('site_name_url'),
                settings.FREE_BASICS_MOLO_SITE_DOMAIN)
        )
        serializer.save(controller=controller)
        tasks.start_new_controller.delay(controller.id)


class TemplateDataManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = FreeBasicsTemplateData.objects.all()
    serializer_class = FreeBasicsDataSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.controller.name = instance.site_name
        instance.controller.domain_urls = '%s.%s' % (
            instance.site_name_url,
            settings.FREE_BASICS_MOLO_SITE_DOMAIN)
        instance.controller.save()
        update_marathon_app.delay(instance.controller.id)


class FreeBasicsHomepageView(HomepageView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            user_orgs = Organization.objects.for_user(request.user)
            if not self.get_queryset().exists() and user_orgs.exists():
                return redirect(reverse('freebasics_add'))
        else:
            if not self.get_queryset().exists():
                return redirect(reverse('freebasics_add'))

        return super(
            FreeBasicsHomepageView, self).dispatch(request, *args, **kwargs)


class FreeBasicsControllerCreateView(ControllerCreateView):
    template_name = 'freebasics_controller_edit.html'
    permissions = ['controllers.docker.add_dockercontroller']


class FreeBasicsControllerEditView(ControllerEditView):
    template_name = 'freebasics_controller_edit.html'
    permissions = ['controllers.docker.add_dockercontroller']
