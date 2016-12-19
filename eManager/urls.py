from django.conf.urls import include, url
from django.contrib import admin

from . import views

app_name = 'emanager'

urlpatterns = [
	url(r'^$', views.EventsListView.as_view(), name='index'),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetailsView.as_view(), name='event_detail'),
    url(r'^events/(?P<pk>[0-9]+)/comment/(?P<comment_id>[0-9]+)/', views.EventDetailsView.as_view(), name='event_detail_with_comment'),
    url(r'^events/(?P<pk>[0-9]+)/edit/$', views.EventEditView.as_view(), name='event_edit'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^add_comment/(?P<pk>[0-9]+)/$', views.AddComment, name='AddComment'),
    url(r'^delete_comment/(?P<pk>[0-9]+)/$', views.DeleteComment, name='DeleteComment'),
    url(r'^change_comment/(?P<pk>[0-9]+)/$', views.ChangeComment, name='ChangeComment'),
]