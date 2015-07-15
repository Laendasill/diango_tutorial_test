from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search-form/$', views.search_form),
    url(r'^(?P<question_id>[0-9]+)/edit/$', views.edit, name='edit'),
]
