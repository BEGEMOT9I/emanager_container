#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views import generic
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Auth form and helper for working with user session
from django.contrib.auth import login, logout, authenticate
from .models import Event, MyUser
from .forms import UserCreationForm as RegistrationForm

class EventsListView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'

	def get_context_data(self, **kwargs):
		context = super(EventsListView, self).get_context_data(**kwargs)
		context['is_logined'] = self.request.user.is_authenticated()
		return context

	def get_queryset(self):
		return Event.objects.order_by('start_date')

class EventDetailsView(generic.DetailView):
	model = Event
	template_name = 'eManager/detail.html'

class RegistrationView(generic.edit.CreateView):
	model = MyUser
	form_class = RegistrationForm
	template_name = 'eManager/registration.html'

	def form_valid(self, form):
		return super(RegistrationView, self).form_valid(form)

	def get_success_url(self):
		return '/login/'

class LoginView(generic.edit.FormView):
	model = MyUser
	form_class = AuthenticationForm
	template_name = 'eManager/login.html'
	success_url = "/"

	def form_valid(self, form):
		self.user = form.get_user()
		login(self.request, self.user)
		return super(LoginView, self).form_valid(form)

	def form_invalid(self, form):
		print 'invalid'
		return super(LoginView, self).form_invalid(form)

class LogoutView(generic.base.View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect("/")