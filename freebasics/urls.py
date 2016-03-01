from django.conf.urls import patterns, url, include

from freebasics import views


urlpatterns = patterns(
    '',
    url(r'^', include('mc2.urls')),
    url(
        r'^add/$',
        views.FreeBasicsControllerCreateView.as_view(),
        name='freebasics_add'
    ),
    url(
        r'^(?P<controller_pk>\d+)/$',
        views.FreeBasicsControllerEditView.as_view(),
        name='freebasics_edit'),
)
