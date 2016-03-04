import json

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def template_data_api_stub(request):
    if request.method == 'POST':
        json.loads(request.body)
        data = {'success': True}
    else:
        data = {
            "general": {
                "siteName": "Happy Place",
                "siteNameUrl": "happy-place"
            },
            "styles": {
                "base-bcolor": {"background-color": "#efefef"},
                "fb-body": {
                    "font-family": '"Open Sans", Helvetica, sans-serif'},
                "block-heading": {
                    "background-color": "#dfdfdf",
                    "font-family": '"Montserrat", Courier, monospace',
                    "text-transform": "uppercase"
                },
                "fb-accent-1": {"color": "#69269d"},
                "fb-accent-2": {"color": "#c736c0"}
            },
            "blocks": {
                "fb-block-header": {"position": 0},
                "fb-block-article": {"position": 2},
                "fb-block-banner": {"position": 3},
                "fb-block-category": {"position": 1},
                "fb-block-poll": {"position": 4},
                "fb-block-footer": {"position": 5}
            }
        }
    return HttpResponse(json.dumps(data), content_type='application/json')
