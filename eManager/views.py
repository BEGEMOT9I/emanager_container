from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Event

class MainView(generic.ListView):
	template_name = 'eManager/index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.order_by('start_date')

class DetailView(generic.DetailView):
	model = Event
	template_name = 'eManager/detail.html'

def index(request):
	print('Index template')
	return HttpResponse("Hello, world. You're at the polls index.")
