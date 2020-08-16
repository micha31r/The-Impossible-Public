import datetime, random
from django.conf import settings
from background_task import background
from background_task.models import Task
from templated_email import send_templated_mail

from newsletter.models import Subscriber

from idea.models import Idea

from the_impossible.utils import *

# Send email to users every week
@background(schedule=0)
def explore_email():
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

	#Must send email one by one to keep users' email address hidden
	for sub in subscribers:
		send_templated_mail(
			template_name='explore',
			from_email=settings.EMAIL_HOST_USER,
			recipient_list=[sub.email],
			context={
				'date':date,
				'from_date':timestamp_from,
			    'to_date':timestamp_to,
			    'weekly_ideas':weekly_ideas,
			    'random_ideas':random_ideas,
			    'subscriber_slug':sub.slug,
			},
		)
		sub.last_sent = today
		sub.save()

explore_email(repeat=Task.WEEKLY, repeat_until=None)