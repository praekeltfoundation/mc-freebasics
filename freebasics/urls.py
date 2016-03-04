from django.conf.urls import patterns, url, include

from freebasics import views


urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.FreeBasicsHomepageView.as_view(),
        name='home'
    ),
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
    url(r'^api_stub/$', views.template_data_api_stub, name='api_stub'),
)
