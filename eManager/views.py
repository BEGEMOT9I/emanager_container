#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import Event, User

class UserForm(forms.Form):
	login = forms.CharField(label = 'login')

class EventsListView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.order_by('start_date')

class EventDetailsView(generic.DetailView):
	model = Event
	template_name = 'eManager/detail.html'

class RegisterView(generic.edit.CreateView):
	model = User
	fields = ['login', 'password']
	template_name = 'eManager/register.html'

	def form_valid(self, form):
		instance = form.save(commit = False)
		users = User.objects.filter(login=instance.login)

		if users.count():
			form.error = 'Пользователь с данным логином уже существует'
			return super(RegisterView, self).form_invalid(form)
		else:
			form.save()
			return super(RegisterView, self).form_valid(form)

	def get_success_url(self):
		return '/login/'

class LoginView(generic.edit.FormView):
	form_class = AuthenticationForm
	template_name = 'eManager/login.html'