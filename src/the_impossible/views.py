from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .utils import *

# Home page
def home_page(request):
	ctx = {}
	ctx["date"] = Date()
	template_file = "home.html"
	return render(request,template_file,ctx)

def access_error_page(request):
	ctx = {}
	template_file = "access_error.html"
	return render(request,template_file,ctx)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def robots_txt(request):
	text = open(settings.BASE_DIR+'/the_impossible/templates/robots.txt', 'r')
	return HttpResponse(text, content_type='text/plain')
