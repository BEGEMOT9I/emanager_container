#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django import forms, template

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

# Auth form and helper for working with user session
from django.contrib.auth import login, logout, authenticate
from .models import Event, MyUser, Comment, Organization
from .forms import UserCreationForm as RegistrationForm, EventCreateForm
import quickstart

# Comment block

def AddComment(request, pk):
	if request.method == 'POST' and request.user.is_authenticated:
		event = Event.objects.filter(pk=pk).first()
		user = request.user
		text = request.POST['text']
		instance = Comment.objects.create_comment(event, user, text)
		return redirect('emanager:event_detail_with_comment', pk=event.id, comment_id=instance.id)
		
	return HttpResponseRedirect('/')

def ChangeComment(request, pk):
	if request.method == 'POST' and request.user.is_authenticated:
		text = request.POST['new_text']
		errors = []

		if not text:
			errors.append('Пустой текст')

		comments = Comment.objects.filter(pk=pk, user_id=request.user.id)

		if not comments:
			errors.append('Нет коммента')

		if not len(errors):
			comments.update(text=text)

		return JsonResponse({'errors': errors})

	return HttpResponseRedirect('/')

def DeleteComment(request, pk):
	if request.user.is_authenticated:
		comment = Comment.objects.filter(pk=pk, user_id=request.user.id).first()
		event_id = comment.event_id
		comment.delete()
		return redirect('emanager:event_detail', pk=event_id)

	return HttpResponseRedirect('/')

# Event block

class EventCreateView(LoginRequiredMixin, generic.edit.CreateView):
	model = Event
	template_name = 'eManager/event/add.html'
	form_class = EventCreateForm

	def get_form_kwargs(self):
		kwargs = super(EventCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.user = self.request.user
		instance.organization_id = form.cleaned_data['organization'].id
		instance.save()
		return super(EventCreateView, self).form_valid(form)

	def get_success_url(self):
		return '/profile/'

class EventEditView(LoginRequiredMixin, generic.edit.UpdateView):
	model = Event
	template_name = 'eManager/event/edit.html'
	form_class = EventCreateForm

	def get_form_kwargs(self):
		kwargs = super(EventEditView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.user = self.request.user
		instance.organization_id = form.cleaned_data['organization'].id
		instance.save()
		return super(EventEditView, self).form_valid(form)

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
		context['event'].comments = Comment.objects.filter(event_id=context['event'].id)

		for comment in context['event'].comments:
			comment.username = MyUser.objects.filter(id=comment.user_id).first()

		return context

def DeleteEvent(request, pk):
	if request.user.is_authenticated:
		event = Event.objects.filter(pk=pk, user_id=request.user.id).first()
		event.delete()
		return redirect('emanager:UserEventsView')

	return HttpResponseRedirect('/')

class EventsListView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'
	paginate_by = 3

	def get_queryset(self):
		return Event.objects.order_by('start_date')
		
def ShareEvent(request, pk):
	event = Event.objects.filter(pk=pk).first()
	quickstart.main(event)
	return redirect('/')

def ChangeRating(request, pk):
	if request.method == 'POST' and request.user.is_authenticated:
		event = Event.objects.filter(pk=pk).first()
		user = request.user
		user_list = event.user_list.encode('ascii','ignore').split(" ")
		count = 0

		if user_list[0] != '':
			for user_in_list in user_list:
				count += 1
				if user_in_list == user.username:
					return redirect('emanager:event_detail', pk=event.id)

		if count > 0:
			event.user_list += ' '

		event.user_list += user.username

		rating = float(event.evaluation)
		count = float(count)
		sumrate = rating * count
		sumrate += float(request.POST['answer'])
		if event.evaluation == 0:
			event.evaluation = 1
			
		event.evaluation = sumrate / (count + 1)
		event.save()

		return redirect('emanager:event_detail', pk=event.id)
	
# Organization block

class OrganizationCreateView(LoginRequiredMixin, generic.edit.CreateView):
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

		if self.request.GET and self.request.GET['next']:
			return HttpResponseRedirect(self.request.GET['next'])
		else:
			return super(LoginView, self).form_valid(form)

	def form_invalid(self, form):
		return super(LoginView, self).form_invalid(form)

class LogoutView(generic.base.View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect("/")

# User page

class UserOrganizationsView(LoginRequiredMixin, generic.base.TemplateView):
	template_name = 'eManager/profile/organizations.html'

	def get_context_data(self, **kwargs):
		context = super(UserOrganizationsView, self).get_context_data(**kwargs)
		context['organizations'] = Organization.objects.filter(creator_id=self.request.user.id)

		return context

class UserEventsView(LoginRequiredMixin, generic.base.TemplateView):
	template_name = 'eManager/profile/events.html'

	def get_context_data(self, **kwargs):
		context = super(UserEventsView, self).get_context_data(**kwargs)
		context['events'] = Event.objects.filter(user_id=self.request.user.id)

		return context

class UserCommentsView(LoginRequiredMixin, generic.base.TemplateView):
	template_name = 'eManager/profile/comments.html'

	def get_context_data(self, **kwargs):
		context = super(UserCommentsView, self).get_context_data(**kwargs)
		context['comments'] = Comment.objects.filter(user_id=self.request.user.id)

		for comment in context['comments']:
			comment.event_name = Event.objects.filter(id=comment.event_id).first()

		return context

class UserProfileView(LoginRequiredMixin, generic.base.TemplateView):
	template_name = 'eManager/profile/index.html'