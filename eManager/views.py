#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Auth form and helper for working with user session
from django.contrib.auth import login, logout, authenticate
from .models import Event, MyUser, Comment, Organization
from .forms import UserCreationForm as RegistrationForm

# Comment block

def AddComment(request, pk):
	if request.method == 'POST':
		event = Event.objects.filter(pk=pk).first()
		user = request.user
		text = request.POST['text']
		instance = Comment.objects.create_comment(event, user, text)
		return redirect('emanager:event_detail_with_comment', pk=event.id, comment_id=instance.id)
		
	return HttpResponseRedirect('/')

def ChangeComment(request, pk):
	if request.method == 'POST':
		text = request.POST['new_text']
		errors = []

		if not text:
			errors.append('Пустой текст')

		comments = Comment.objects.filter(pk=pk)

		if not comments:
			errors.append('Нет коммента')

		if not len(errors):
			comments.update(text=text)

		return JsonResponse({'errors': errors})

def DeleteComment(request, pk):
	comment = Comment.objects.filter(pk=pk).first()
	event_id = comment.event_id
	comment.delete()
	return redirect('emanager:event_detail', pk=event_id)

# Event block

class EventCreateView(generic.edit.CreateView):
	model = Event
	template_name = 'eManager/event/add.html'
	fields = ['organization', 'name', 'start_date', 'description', 'address', 'image']

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.user = self.request.user
		instance.save()
		return super(EventCreateView, self).form_valid(form)

	def get_success_url(self):
		return '/profile/'

class EventEditView(generic.edit.UpdateView):
	model = Event
	template_name = 'eManager/event/edit.html'
	fields = ['organization', 'name', 'start_date', 'description', 'address', 'image']

	def get_context_data(self, **kwargs):
		context = super(EventEditView, self).get_context_data(**kwargs)
		return context

	def get_success_url(self):
		return '/'

class EventDetailsView(generic.DetailView):
	model = Event
	template_name = 'eManager/event/detail.html'

	def get_context_data(self, **kwargs):
		context = super(EventDetailsView, self).get_context_data(**kwargs)
		# context['event'].organization = Organization.objects.filter(id=context['event'].organization_id).first().name
		context['event'].comments = Comment.objects.filter(event_id=context['event'].id)
		for comment in context['event'].comments:
			comment.username = MyUser.objects.filter(id=comment.user_id).first()

		return context

def DeleteEvent(request, pk):
	event = Event.objects.filter(pk=pk).first()
	event.delete()
	return redirect('emanager:UserEventsView')

class EventsListView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.order_by('start_date')

# Organization block

class OrganizationCreateView(generic.edit.CreateView):
	model = Organization
	template_name = 'eManager/organization/add.html'
	fields = ['name', 'description', 'image']

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.creator = self.request.user
		instance.save()
		return super(OrganizationCreateView, self).form_valid(form)

	def get_success_url(self):
		return '/profile/'

# Registration and authentication

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

# User page

class UserOrganizationsView(generic.base.TemplateView):
	template_name = 'eManager/profile/organizations.html'

	def get_context_data(self, **kwargs):
		context = super(UserOrganizationsView, self).get_context_data(**kwargs)
		context['organizations'] = Organization.objects.filter(creator_id=self.request.user.id)

		return context

class UserEventsView(generic.base.TemplateView):
	template_name = 'eManager/profile/events.html'

	def get_context_data(self, **kwargs):
		context = super(UserEventsView, self).get_context_data(**kwargs)
		context['events'] = Event.objects.filter(user_id=self.request.user.id)

		return context

class UserCommentsView(generic.base.TemplateView):
	template_name = 'eManager/profile/comments.html'

	def get_context_data(self, **kwargs):
		context = super(UserCommentsView, self).get_context_data(**kwargs)
		context['comments'] = Comment.objects.filter(user_id=self.request.user.id)

		for comment in context['comments']:
			comment.event_name = Event.objects.filter(id=comment.event_id).first()

		return context

class UserProfileView(generic.base.TemplateView):
	template_name = 'eManager/profile/index.html'