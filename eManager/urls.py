from django.conf.urls import include, url
from django.contrib import admin

from . import views

app_name = 'emanager'

urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', views.DetailView, name='detail'),
]