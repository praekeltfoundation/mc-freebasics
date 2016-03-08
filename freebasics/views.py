from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from mc2.controllers.base.views import ControllerCreateView, ControllerEditView
from mc2.views import HomepageView
from freebasics.forms import FreeBasicsControllerForm

from freebasics.models import FreeBasicsTemplateData, FreeBasicsController
from freebasics.serializers import FreeBasicsDataSerializer

from rest_framework import generics


class TemplateDataCreate(generics.ListCreateAPIView):
    queryset = FreeBasicsTemplateData.objects.all()
    serializer_class = FreeBasicsDataSerializer

    def perform_create(self, serializer):
        print 'perform create'
        controller = FreeBasicsController.objects.create(
            owner=self.request.user)
        serializer.save(controller=controller)


class TemplateDataManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = FreeBasicsTemplateData.objects.all()
    serializer_class = FreeBasicsDataSerializer


class FreeBasicsHomepageView(HomepageView):

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return redirect(reverse('freebasics_add'))
        return super(
            FreeBasicsHomepageView, self).dispatch(request, *args, **kwargs)


class FreeBasicsControllerCreateView(ControllerCreateView):
    form_class = FreeBasicsControllerForm
    template_name = 'freebasics_controller_edit.html'
    permissions = ['controllers.docker.add_dockercontroller']


class FreeBasicsControllerEditView(ControllerEditView):
    form_class = FreeBasicsControllerForm
    template_name = 'freebasics_controller_edit.html'
    permissions = ['controllers.docker.add_dockercontroller']
