#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms

# Auth form and helper for working with user session
from django.middleware.csrf import rotate_token
from django.contrib.auth import _get_user_session_key, SESSION_KEY, HASH_SESSION_KEY, login, authenticate

from .models import Event, User

# Rewriting old session key
def monkey_patch_login(request, user):
	session_auth_hash = ''
	if user is None:
		user = request.user
	if hasattr(user, 'get_session_auth_hash'):
		session_auth_hash = user.get_session_auth_hash()

	if SESSION_KEY in request.session:
		if _get_user_session_key(request) != user.pk or (
				session_auth_hash and
				request.session.get(HASH_SESSION_KEY) != session_auth_hash):
			request.session.flush()
	else:
		request.session.cycle_key()

	request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
	request.session[HASH_SESSION_KEY] = session_auth_hash

	if hasattr(request, 'user'):
		request.user = user
	rotate_token(request)

login = monkey_patch_login

class AuthenticationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'

class UserForm(forms.Form):
	login = forms.CharField(label = 'login')

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
	model = User
	fields = ['login', 'password']
	template_name = 'eManager/registration.html'

	def form_valid(self, form):
		instance = form.save(commit = False)
		users = User.objects.filter(login=instance.login)

		if users.count():
			form.error = 'Пользователь с данным логином уже существует'
			return super(RegistrationView, self).form_invalid(form)
		else:
			form.save()
			return super(RegistrationView, self).form_valid(form)

	def get_success_url(self):
		return '/login/'

class LoginView(generic.edit.FormView):
	model = User
	form_class = AuthenticationForm
	template_name = 'eManager/login.html'
	success_url = "/"

	def form_valid(self, form):
		print 'valid'
		instance = form.save(commit = False)
		users = User.objects.filter(login = instance.login, password = instance.password)

		if users.count() == 1:
			user = users.first()
			authenticate(username=user.login, password=user.password)
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			form.error = 'Неправильный логин/пароль'
			return super(LoginView, self).form_invalid(form)

	def form_invalid(self, form):
		print 'invalid'
		form.error = 'Неправильный логин/пароль'
		return super(LoginView, self).form_invalid(form)