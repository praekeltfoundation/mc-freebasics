from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from mc2.controllers.base.views import ControllerCreateView, ControllerEditView
from mc2.views import HomepageView
from freebasics.forms import FreeBasicsControllerForm


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
