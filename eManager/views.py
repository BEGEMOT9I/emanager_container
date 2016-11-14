from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Event


def MainView(request):
	event_list = Event.objects.order_by('-start_date')
	context = {'event_list': event_list}
	return render(request, 'eManager/index.html', context)

def DetailView(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		raise Http404("Event doesn`t exist")
	context = {'event': event}
	return render(request, 'eManager/detail.html', context)