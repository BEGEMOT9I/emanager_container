from django.http import HttpResponse


def index(request):
	print 'Index template'
	print('Index template')
	return HttpResponse("Hello, world. You're at the polls index.")
