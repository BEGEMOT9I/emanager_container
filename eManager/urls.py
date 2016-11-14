from django.conf.urls import include, url
from django.contrib import admin

from . import views

app_name = 'emanager'

urlpatterns = [
	url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]