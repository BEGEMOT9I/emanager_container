#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Auth form and helper for working with user session
from django.contrib.auth import login, logout, authenticate
from .models import Event, MyUser, Comment
from .forms import UserCreationForm as RegistrationForm

class EventsListView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.order_by('start_date')

def AddComment(request, pk):
	if request.method == 'POST':
		event = Event.objects.filter(pk=pk).first()
		user = request.user
		text = request.POST['text']
		instance = Comment.objects.create_comment(event, user, text)
		return redirect('emanager:detail_with_comment', pk=event.id, comment_id=instance.id)
		
	return HttpResponseRedirect('/')

def DeleteComment(request, pk):
	comment = Comment.objects.filter(pk=pk).first()
	event_id = comment.event_id
	comment.delete()
	return redirect('emanager:detail', pk=event_id)

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

class EventDetailsView(generic.DetailView):
	model = Event
	template_name = 'eManager/detail.html'

	def get_context_data(self, **kwargs):
		context = super(EventDetailsView, self).get_context_data(**kwargs)
		context['event'].comments = Comment.objects.filter(event_id=context['event'].id)
		for comment in context['event'].comments:
			comment.username = MyUser.objects.filter(id=comment.user_id).first()

		return context

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