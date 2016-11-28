from django.conf.urls import include, url
from django.contrib import admin

from . import views

app_name = 'emanager'

urlpatterns = [
	url(r'^$', views.EventsListView.as_view(), name='index'),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetailsView.as_view(), name='detail'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login')
]