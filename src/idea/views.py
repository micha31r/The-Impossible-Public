from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime, random

from the_impossible.utils import *

from .forms import *

from .utils import *

from the_impossible.ERROR import *

from usermgmt.models import (
	Notification,
	Profile,
)

from support.models import CoreFeed

from .models import (
	Tag, 
	Idea,
	Comment
)

# MINIMUM_DATE = datetime.datetime.date(datetime.datetime(2020, 4, 9))
IDEA_PER_PAGE = 12
COMMENT_PER_PAGE = 3

# Idea related

def explore_page(request,week_num,page_num):
	ctx = {} # Context variables
	ctx["date"] = date = Date()
	ctx["week_num"] = week_num
	# Check if week_num is valid
	if week_num > current_week() or week_num < 0: raise Http404()
	ctx["page_num"] = page_num
	today = date.now()
		
	fav_tags = None # For discover section idea filter
	if request.user.is_authenticated:
		ctx["profile"] = profile = get_object_or_404(Profile, user=request.user)
		# Count unread notifications
		ctx["new_notification"] = profile.notification.filter(dismissed=False).count()
		# Set favourite tags
		if profile.tags.all():
			fav_tags = profile.tags.all()

	# Explore Section
	# Note: current date is not normal date format, its year/week/1
	current_date = int_date(f"{today.strftime('%Y')}-{week_num}-1")
	ctx['from_date'] = timestamp_from = current_week_dates(*current_date)
	ctx['to_date'] = timestamp_to = timestamp_from + datetime.timedelta(days=7)
	# Check if there is previous or next week
	if week_num > 0: ctx["previous_week_num"] = week_num - 1
	if week_num < current_week(): ctx["next_week_num"] = week_num + 1

	# Filter by date
	# https://stackoverflow.com/questions/4923612/filter-by-timestamp-in-query
	ideas = Idea.objects.filter(
		timestamp__gte = timestamp_from,
		timestamp__lt = timestamp_to,
		publish_status = 3
	).distinct().order_by("id").reverse()
	# Split data into pages
	ideas = Paginator(ideas,IDEA_PER_PAGE)
	ctx["max_page"] = ideas.num_pages
	try: current_page = ideas.page(page_num) # Get the ideas on the current page
	except: raise Http404()
	ctx["masonary_ideas"] = current_page 

	# Discover Section
	# Retrieve all ideas from the past 6 months
	if request.user.is_authenticated and profile.use_tag_filter == 2 and fav_tags:
		ideas = Idea.objects.filter(
			timestamp__gte = date.now() - datetime.timedelta(days=182),
			timestamp__lte = date.now() + datetime.timedelta(days=1),
			publish_status = 3,
			tags__in=fav_tags
		).exclude(header_img=None).distinct()
	else:
		ideas = Idea.objects.filter(
			timestamp__gte = date.now() - datetime.timedelta(days=182),
			timestamp__lte = date.now() + datetime.timedelta(days=1),
			publish_status = 3,
		).exclude(header_img=None).distinct()
	ctx["random_ideas"] = random.sample(list(ideas), min(ideas.count(), 10))

	template_file = "idea/explore.html"
	return render(request,template_file,ctx)

@login_required
def feed_page(request):
	ctx = {}
	ctx["date"] = date = Date()
	ctx["profile"] = profile = get_object_or_404(Profile, user=request.user)
	
	# Recent published ideas by followed users
	ctx["recent_ideas"] = Idea.objects.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=60),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
		author__user__in=profile.following.all()
	).exclude(publish_status=1).distinct().order_by("-timestamp")[:20]
	# Recent public messages by the admin of this site 
	core_feed_public = CoreFeed.objects.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=30),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
		publish_status = 2
	).distinct().order_by("-timestamp")[:10]
	# Recent private messages by this site 
	core_feed_private = profile.core_feed.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=30),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
	).distinct().order_by("-timestamp")[:10]
	ctx["core_feed"] = (core_feed_public | core_feed_private).order_by("-timestamp") # Merge qs

	template_file = "idea/feed.html"
	return render(request,template_file,ctx)

@login_required
def detail_page(request,pk):
	ctx = {} # Context variables
	ctx["date"] = Date()
	ctx["idea"] = idea = get_object_or_404(Idea, pk=pk)
	# Add view count
	ctx["profile"] = profile = get_object_or_404(Profile, user=request.user)
	idea.viewed_user.add(profile)

	# Comment relate stuff
	ctx["comments"] = idea.comments.all().order_by("-timestamp")[:COMMENT_PER_PAGE]
	ctx["total_comments_num"] = idea.comments.all().count()
	ctx["form"] = form = CommentForm(request.POST or None)

	if form.is_valid():
		data = form.cleaned_data
		comment = Comment.objects.create(
			author = profile,
			content = data.get("content")
		)
		comment.save()
		idea.comments.add(comment)
		idea.save()

		# Notify the author	about the comment
		if idea.author.comment_setting != 1:
			proceed = False
			if idea.author.comment_setting == 2:
				followers = User.objects.filter(profile__following=idea.author.user) # The author's followers
				if profile.user in followers:
					proceed = True
			elif idea.author.comment_setting == 3:
				proceed = True
			if proceed:
				absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(profile.user.username,'my',1)))
				message = f"<a href='{absolute_url}'>@{profile.user.username}</a> has commented on your post <a href='{request.path}'>\"{idea.name}\"</a>"
				msg = Notification.objects.create(message=message,message_status=1)
				msg.save()
				idea.author.notification.add(msg)
				idea.author.save()

		# Search description for @ users
		usernames = at_filter(comment.content)
		for username in usernames:
			user = User.objects.filter(username=username).first()
			if user:
				profile = Profile.objects.filter(user=user).first()
				# Send the mentioned user a notification
				absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(request.user.username,'my',1)))
				message = f"<a href='{absolute_url}'>@{request.user.username}</a> mentioned you in a comment in <a href='{request.path}'>\"{idea.name}\"</a>"
				msg = Notification.objects.create(message=message,message_status=2)
				msg.save()
				# Notify mentioned user
				profile.notification.add(msg)
			else: 
				# Tell the current user that their mentioned user does not exist
				message = f"@{username} user does not exist"
				msg = Notification.objects.create(message=message,message_status=1)
				msg.save()
				idea.author.notification.add(msg)
				idea.author.save()

		# Clear form
		ctx["form"] = CommentForm()

	template_file = "idea/detail.html"
	return render(request,template_file,ctx)

@login_required
def create_view(request):
	date = Date()
	profile = get_object_or_404(Profile,user=request.user)
	
	if profile.daily_limit_timestamp.strftime("%Y-%m-%d") == str(date.now()):
		if profile.daily_limit <= 0:
			return redirect("idea:limit_page")
	else:
		profile.daily_limit = 5
		profile.daily_limit_timestamp = date.now()
		profile.save()
	
	obj = Idea.objects.create(
		name="untitled",
		short_description="",
		full_description="",
		author=profile
	)
	obj.save()
	profile.daily_limit -= 1
	profile.save()
	return redirect("idea:edit_page",pk=obj.id)

# Daily limit reached
def limit_page(request):
	ctx = {}
	template_file = "idea/limit.html"
	return render(request,template_file,ctx)

@login_required
def edit_page(request,pk):
	ctx = {} # Context variables
	ctx["date"] = date = Date()
	ctx["idea"] = idea = get_object_or_404(Idea, pk=pk)
	if idea.author.user == request.user:
		ctx["form"] = form = IdeaForm(request.POST or None)
		# Set default values
		form.fields["name"].initial = idea.name
		form.fields["short_description"].initial = idea.short_description
		form.fields["full_description"].initial = idea.full_description
		form.fields["tags"].queryset = idea.tags
		form.fields["publish_status"].initial = idea.publish_status
		# Show avaliable tags
		qs = Tag.objects.all().distinct()
		for tag in idea.tags.all():
			qs = qs.exclude(name=tag.name)
		ctx["tags"] = qs
		form.fields["tags_remain"].widget = forms.SelectMultiple(choices=[(choice.id, choice) for choice in qs])
		
		usernames_before_edit = at_filter(idea.full_description)

		# Form validation
		if form.is_valid():
			data = form.cleaned_data
			if data.get("delete") == 2:
				idea.delete()
				return redirect("idea:explore_page",date.week(),1)

			idea.name = escape_html(data.get("name"))
			idea.short_description = data.get("short_description")

			idea_absolute_url = request.build_absolute_uri(reverse('idea:detail_page', args=(pk,)))

			# Search description for @ users
			usernames = set(at_filter(data.get("full_description"))) - set(usernames_before_edit)
			for username in usernames:
				user = User.objects.filter(username=username).first()
				if user:
					proceed = False
					# You can only mention users if they follow you or the post is public
					followers =  User.objects.filter(profile__following=idea.author.user)
					if (data.get("publish_status") == 2 and user in followers) or data.get("publish_status") == 3:
						proceed = True
					if proceed:
						profile = Profile.objects.filter(user=user).first()
						# Send the mentioned user a notification
						user_absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(request.user.username,'my',1)))
						message = f"<a href='{user_absolute_url}'>@{request.user.username}</a> mentioned you in <a href='{idea_absolute_url}'>\"{idea.name}\"</a>"
						msg = Notification.objects.create(message=message,message_status=2)
						msg.save()
						# Notify mentioned user
						profile.notification.add(msg)
					else:
						# Tell the current user that certain uses can't be mentioned
						user_absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(username,'my',1)))
						message = f"<a href='{user_absolute_url}'>@{username}</a> is not mentioned due to <a href='{idea_absolute_url}'>\"{idea.name}\"</a>s publish setting"
						msg = Notification.objects.create(message=message,message_status=1)
						msg.save()
						idea.author.notification.add(msg)
						idea.author.save()
						# Remove username from description
						data["full_description"] = data["full_description"].replace(f"@{username}","")
				else: 
					# Tell the current user that their mentioned user does not exist
					message = f"@{username} user does not exist"
					msg = Notification.objects.create(message=message,message_status=1)
					msg.save()
					idea.author.notification.add(msg)
					idea.author.save()

			idea.full_description = data.get("full_description")

			# Change publish setting
			idea.publish_status = data.get("publish_status")

			# Notify followers if publish setting is set to followers-only or public
			if not idea.notified and (idea.publish_status == 2 or idea.publish_status == 3):
				idea.notified = True
				user_absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(request.user.username,'my',1)))
				message = f"<a href='{user_absolute_url}'>@{request.user.username}</a> has created a new post <a href='{idea_absolute_url}'>\"{idea.name}\"</a>"
				msg = Notification.objects.create(message=message,message_status=1)
				msg.save()
				followers = User.objects.filter(profile__following=idea.author.user)
				for follower in followers.all():
					follower_profile = get_object_or_404(Profile, user=follower)
					follower_profile.notification.add(msg)
					follower_profile.save()

			# Add tags
			for tag in eval(data.get('tags_remain') or "[]"): # convert
				idea.tags.add(tag)
			# Remove tags
			for tag in data.get('tags'):
				idea.tags.remove(tag)

			idea.save()

			if request.POST.get("redirect_img"):
				# Redirect to file page
				return redirect(request.POST.get("redirect_img"))
			else:
				# Refresh page
				return redirect("idea:edit_page", pk=idea.id)
	else:
		return redirect("access_error_page")
	template_file = "idea/edit.html"
	return render(request,template_file,ctx)

def search_page(request,page_num,name):
	ctx = {}
	ctx["date"] = date = Date()
	if name == "None":
		name = request.GET.get('name',None)
	if name:
		ctx["name"] = name
		ctx["page_num"] = page_num
		if request.user.is_authenticated:
			ctx["profile"] = get_object_or_404(Profile,user=request.user)
		ideas = Idea.objects.filter(name__icontains=name).order_by("-timestamp")
		if ideas.count() > 0:
			ctx["entry_count"] = ideas.count()
			# Split data into pages
			ideas = Paginator(ideas,IDEA_PER_PAGE)
			ctx["max_page"] = ideas.num_pages
			try: current_page = ideas.page(page_num) # Get the ideas on the current page
			except: raise Http404()
			ctx["masonary_ideas"] = current_page 
		else:
			ctx["error"] = SERVER_ERROR["IDEA"]
	template_file = "idea/search.html"
	return render(request,template_file,ctx)

# Star and Like related

@login_required
def like_view(request):
	data = {}
	try:
		if request.is_ajax():
			# Get object pk
			pk = request.GET.get('pk')
			# Retrieve objects
			idea = get_object_or_404(Idea,pk=pk)
			user = get_object_or_404(User,username=request.user.username)
			profile = get_object_or_404(Profile,user=user)
			# Add like
			if idea.liked_user.filter(user=profile.user).exists(): 	
				data["action"] = "unliked"			
				idea.liked_user.remove(profile) 	
			else: 											
				idea.liked_user.add(profile)
				# Notify the author	
				if idea.author.like_setting != 1:
					proceed = False
					if idea.author.like_setting == 2:
						followers = User.objects.filter(profile__following=idea.author.user) # The author's followers
						if profile.user in followers:
							proceed = True
					elif idea.author.like_setting == 3:
						proceed = True
					if proceed:
						user_absolute_url = request.build_absolute_uri(reverse('usermgmt:account_dashboard_page', args=(user.username,'my',1)))
						idea_absolute_url = request.build_absolute_uri(reverse('idea:detail_page', args=(pk,)))
						message = f"<a href='{user_absolute_url}'>@{user.username}</a> has liked your post <a href='{idea_absolute_url}'>\"{idea.name}\"</a>"
						msg = Notification.objects.create(message=message,message_status=1)
						msg.save()
						idea.author.notification.add(msg)
						idea.author.save()
				data["action"] = "liked"
		else:
			raise CustomError("AjaxInvalid")
	except:
		data['failed'] = True
	return JsonResponse(data)

@login_required
def star_view(request):
	data = {}
	try:
		if request.is_ajax():
			# Get object pk
			pk = request.GET.get('pk')
			# Retrieve objects
			idea = get_object_or_404(Idea,pk=pk)
			user = get_object_or_404(User,username=request.user.username)
			profile = get_object_or_404(Profile,user=user)
			# Add like
			if idea.starred_user.filter(user=profile.user).exists(): 	
				data["action"] = "unstarred"		
				idea.starred_user.remove(profile)
			else: 											
				idea.starred_user.add(profile)		
				data["action"] = "starred"			
		else:
			raise CustomError("AjaxInvalid")
	except:
		data['failed'] = True
	return JsonResponse(data)

# Comment related 

@login_required
def comment_delete_view(request,comment_pk,idea_pk):
	comment = get_object_or_404(Comment, pk=comment_pk)
	if comment.author.user == request.user:
		comment.delete()
	return redirect("idea:detail_page", pk=idea_pk)

@login_required
def comment_get_view(request):
	data = {}
	try:
		if request.is_ajax():
			# Get object pk
			pk = request.GET.get('pk')
			comment_num = int(request.GET.get("comment_num"))
			# Retrieve objects
			idea = get_object_or_404(Idea,pk=pk)
			comments = idea.comments.all().order_by("-timestamp")[comment_num:comment_num+COMMENT_PER_PAGE]
			authors = []
			timestamps = []
			for comment in comments:
				authors.append(comment.author.user.get_full_name())
				timestamps.append(comment.last_edit.strftime("%B %d, %Y, %I:%M %p"))
			data["comments"] = serializers.serialize('json', comments)
			data["authors"] = authors
			data["timestamps"] = timestamps
			data["new_comment_num"] = comment_num+COMMENT_PER_PAGE
		else:
			raise CustomError("AjaxInvalid")
	except:
		data['failed'] = True
	return JsonResponse(data, safe=False)