from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from mc2.controllers.base.views import ControllerCreateView, ControllerEditView
from mc2.views import HomepageView
from freebasics.forms import FreeBasicsControllerForm

from freebasics.models import FreeBasicsTemplateData
from freebasics.serializers import FreeBasicsDataSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


class TemplateDataList(APIView):
    def get(self, request, format=None):
        templates = FreeBasicsTemplateData.objects.all()
        serializer = FreeBasicsDataSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FreeBasicsDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetail(APIView):
    """
    Retrieve, update or delete a template instance.
    """
    def get_object(self, pk):
        try:
            return FreeBasicsTemplateData.objects.get(pk=pk)
        except FreeBasicsTemplateData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = FreeBasicsDataSerializer(template)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = FreeBasicsDataSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        template = self.get_object(pk)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
