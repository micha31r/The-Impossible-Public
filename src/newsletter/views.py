from django.shortcuts import render
from django.http import JsonResponse

from .models import Subscriber

from .utils import email_is_valid

def join_view(request):
	data = {}
	email = request.GET.get('email', None)
	if email_is_valid(email) and request.is_ajax():
		# Check if email is already used
		if Subscriber.objects.filter(email=email).exists():
			data['exist'] = True
		else:
			obj = Subscriber.objects.create(email=email,frequency=2)
			obj.save()
	else:
		data['failed'] = True
	return JsonResponse(data)

def unenroll_page(request,slug):
	ctx={}
	obj = Subscriber.objects.filter(slug=slug).first()
	if obj:
		ctx["email"] = obj.email
		obj.delete()
	template_name = "newsletter/unenroll.html"
	return render(request,template_name,ctx)


# THIS IS FOR TESTING ONLY !!
import datetime, random
from django.conf import settings
from background_task import background
from background_task.models import Task
from templated_email import send_templated_mail
from newsletter.models import Subscriber
from idea.models import Idea
from the_impossible.utils import *

def email_page(request):
	date = Date()
	today = date.now()
	timestamp = today - datetime.timedelta(days=7)

	# Free gmail account can only send 500 per day
	email_sum = 500

	"""
		Split weekly_subs evenly with monthly_subs, 
		pick 250 weekly and monthly subscribers per day.
		If there are less than 250 weekly subscribers, then 
		increase the number of monthly subscribers.
	"""
	weekly_subs = Subscriber.objects.filter(
		last_sent__lt = timestamp,
		frequency = 2
	).exclude(frequency=1).distinct()[:250] 
	email_sum -= weekly_subs.count()
	
	monthly_subs = Subscriber.objects.filter(
		last_sent__lt = timestamp,
		frequency = 3
	).exclude(frequency=1).distinct()[:email_sum] 

	# Convert qs to list to prevent MySQL unsupported actions
	subscribers = list(weekly_subs) + list(monthly_subs)

	# Explore Section
	# Note: current date is not normal date format, its year/week/1
	current_date = int_date(f"{today.strftime('%Y')}-{date.week()}-1")
	timestamp_from = current_week_dates(*current_date)
	timestamp_to = timestamp_from + datetime.timedelta(days=7)

	# Filter by date
	# https://stackoverflow.com/questions/4923612/filter-by-timestamp-in-query
	weekly_ideas = Idea.objects.filter(
		timestamp__gte = timestamp_from,
		timestamp__lt = timestamp_to,
		publish_status = 3
	).distinct().order_by("id").reverse()[:5]

	random_ideas = Idea.objects.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=182),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
		publish_status = 3,
	).exclude(header_img=None).distinct()
	random_ideas = random.sample(list(random_ideas), min(random_ideas.count(), 5))

	context={
		'date':date,
		'from_date':timestamp_from,
	    'to_date':timestamp_to,
	    'weekly_ideas':weekly_ideas,
	    'random_ideas':random_ideas,
	    'subscriber_slug':"EGYJMDVEGHSJKM", # example slug
	}
	template_name = "templated_email/explore.email"
	# template_name = "templated_email/explore_awesome.email"
	return render(request,template_name,context)

