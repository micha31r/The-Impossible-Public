import random, re
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django import forms

from .forms import (
	LoginForm,
	SignUpForm,
	VerificationForm,
)

from .models import (
	Profile,
	Verification,
	Notification,
)

from .utils import (
	welcome_email, 
	all_private_notification,
	verification_email
)

from userupload.models import File

from idea.models import Idea

from idea.utils import escape_html

from the_impossible.utils import *

from the_impossible.ERROR import *

from support.utils import create_corefeed

from newsletter.models import Subscriber

IDEA_PER_PAGE = 20
NOTIFICATION_PER_PAGE = 50
USER_PER_PAGE = 20

def signup_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	next_page = request.GET.get("next") # Get url of the next page
	if request.user.is_authenticated:
		return redirect(next_page or "account_dashboard_page", username=request.user.username, content_filter="my", page_num=1) # Redirect to the next page
	ctx["signup_form"] = signup_form = SignUpForm(request.POST or None)
	if signup_form.is_valid():
		# Get form inputs
		first_name = signup_form.cleaned_data.get("first_name")
		last_name = signup_form.cleaned_data.get("last_name")
		username = escape_html(signup_form.cleaned_data.get("username")).replace(" ","_")
		email = signup_form.cleaned_data.get("email")
		password = signup_form.cleaned_data.get("password")
		password_confirmation = signup_form.cleaned_data.get("password_confirmation")
		# Make sure no user has the same username or email
		if not User.objects.filter(username=username, is_active=True).exists():
			# Check if there is unactive users with the same username
			if not User.objects.filter(username=username, is_active=False).exists():
				if not User.objects.filter(email=email).exists():
					if re.match("^[A-Za-z0-9_]*$", username):
						if password == password_confirmation: # Confirm password
							# Create user object
							user = User.objects.create_user(
								username=username,
								email=email,
								password=password,
								is_active=False
							)
							user.first_name = first_name.capitalize()
							user.last_name = last_name.capitalize()
							user.save()

							# Create a profile
							profile = Profile.objects.create(user=user)

							# Create Notification
							message = f"@{username}, welcome to The Impossible. If you have any questions, please contact us"
							msg = Notification.objects.create(message=message,message_status=1)
							msg.save()
							profile.notification.add(msg)

							# Create feed
							absolute_url = request.build_absolute_uri(reverse('account_dashboard_page', args=(username,'my',1)))
							profile.core_feed.add(create_corefeed("WELCOME",username=username, absolute_url=absolute_url))

							# Create verification key
							verification = Verification.objects.create(user=user)
							verification.save()

							# Send user an welcome email 
							welcome_email(user.username,user.email,verification.slug)

							# Add user to subscriber
							sub = Subscriber.objects.create(email=user.email)
							sub.save()
							profile.subscriber = sub
							profile.save()

							# Ask user to verify account
							return redirect("verify_page", username=username)
						else: ctx["error"] = SERVER_ERROR["AUTH_PASSWORD_MATCH"]
					else: ctx["error"] = SERVER_ERROR["AUTH_SIGNUP_USERNAME"]
				else: ctx["error"] = SERVER_ERROR["AUTH_SIGNUP_EMAIL_TAKEN"]
			else:
				# Ask user to verify account
				return redirect("verify_page", username=username)
		else: ctx["error"] = SERVER_ERROR["AUTH_SIGNUP_USERNAME_TAKEN"]
	signup_form = SignUpForm()
	template_file = "usermgmt/signup.html"
	return render(request,template_file,ctx)

def verify_page(request,username):
	ctx={}
	ctx["user"] = user = get_object_or_404(User,username=username,is_active=False)
	verification = get_object_or_404(Verification,user=user)
	ctx["form"] = form = VerificationForm(request.POST or None)
	if form.is_valid():
		verification_code = form.cleaned_data.get("code")
		if verification_code == verification.slug:
			user.is_active = True
			user.save()
			return redirect("login_page")
		else:
			ctx["error"] = SERVER_ERROR["AUTH_CODE"]
	template_file = "usermgmt/verify.html"
	return render(request,template_file,ctx)

def send_code_view(request,username):
	ctx={}
	user = get_object_or_404(User,username=username,is_active=False)
	verification = get_object_or_404(Verification,user=user)
	# Send user an welcome email 
	verification_email(user.email,verification.slug)
	return redirect("verify_page",username)

# This page is for DEBUG ONLY !!
def email_page(request):
	ctx={}
	ctx["date"] = Date()
	ctx["verification_code"] = "F28cwJ" # Fake verification code
	template_file = "templated_email/verification.email"
	return render(request,template_file,ctx)

def login_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	next_page = request.GET.get("next") # Get url of the next page
	if request.user.is_authenticated:
		return redirect(next_page or "account_dashboard_page", username=request.user.username, content_filter="my", page_num=1) # Redirect to the next page
	login_form = LoginForm(request.POST or None)
	ctx["login_form"] = login_form
	if login_form.is_valid():
		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")
		user = get_object_or_404(User,username=username)
		if not user.is_active:
			# Ask user to verify account
			return redirect("verify_page", username=username)
		# Validate username with password
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect(next_page or "account_dashboard_page", username=user.username, content_filter="my", page_num=1) # Redirect to the next page
		else: 
			# Display error if user is not found
			ctx["error"] = SERVER_ERROR["AUTH_LOGIN"]
	login_form = LoginForm()
	template_file = "usermgmt/login.html"
	return render(request,template_file,ctx)

@login_required
def logout_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	template_file = "usermgmt/logout.html"
	return render(request,template_file,ctx)

@login_required
def logout_view(request):
    logout(request)
    return redirect("login_page")

def account_dashboard_page(request,username,content_filter,page_num):
	ctx = {}
	ctx["date"] = Date()
	ctx["page_num"] = page_num
	# Created ideas, liked ideas or starred ideas 
	ctx["content_filter"] = content_filter
	ctx["username"] = username
	user = get_object_or_404(User, username=username) # Target user
	# The profile for the logged in user
	if request.user.is_authenticated:
		ctx["profile"] = get_object_or_404(Profile,user=request.user)
	# The profile for the viewed user
	ctx["target_profile"] = target_profile = get_object_or_404(Profile,user=user,user__is_active=True)
	
	# Get 50 most recent notifications
	ctx["target_notifications"] = target_notifications = target_profile.notification.all().order_by('-pk')[:NOTIFICATION_PER_PAGE]
	# Check if all notifications are private
	ctx["all_private"] = all_private_notification(target_notifications)

	# Count unread notifications
	if request.user.is_authenticated and request.user == user:
		ctx["new_notification"] = target_profile.notification.filter(dismissed=False).count()
	# Dismiss notifications
	ctx["undismissed_notifications"] = []
	if request.user == user:
		for notification in target_notifications:
			if not notification.dismissed:
				ctx["undismissed_notifications"].append(notification)
				notification.dismissed = True
				notification.save()

	# Get followers' profiles
	ctx["followers"] = followers = User.objects.filter(profile__following=target_profile.user)
	ctx["followers_profile"] = []
	for follower in followers[:30]:
		ctx["followers_profile"].append(Profile.objects.filter(user=follower).first())

	ideas = {}
	if content_filter == "my": # Ideas created by this user
		# Show all ideas is the current user is the same as the target user
		if request.user.is_authenticated and request.user == user:
			ideas = Idea.objects.filter(author=target_profile).order_by("timestamp").reverse()
		# If the current user follows the target user
		elif request.user.is_authenticated and ctx["profile"].following.filter(username=target_profile.user.username).exists():
			ideas = Idea.objects.filter(author=target_profile).exclude(publish_status=1).order_by("timestamp").reverse()
		else:
			ideas = Idea.objects.filter(author=target_profile, publish_status=3).order_by("timestamp").reverse()
	elif content_filter == "liked":
		# Blocked users can't see this page
		if target_profile.blocked_user.filter(username=request.user.username).exists():
			return redirect("access_error_page")
		# Liked ideas 
		ideas = Idea.objects.filter(liked_user=target_profile)
	elif content_filter == "starred":
		if user == request.user: # Starred ideas are private
			# Starred ideas 
			ideas = Idea.objects.filter(starred_user=target_profile)
		else: return redirect("access_error_page")
	else: raise Http404()

	# Split data into pages
	ideas = Paginator(ideas,IDEA_PER_PAGE)
	ctx["max_page"] = ideas.num_pages
	try: current_page = ideas.page(page_num) # Get the ideas on the current page
	except: raise Http404()
	# On the liked page, remove idea if the current user did not follow the idea's author
	# The filter is done here to optimise performance
	if content_filter == "liked" and user != request.user and request.user.is_authenticated:
		for idea in current_page:
			if not ctx["profile"].following.filter(username=idea.author.user.username).exists():
				current_page.object_list.remove(idea)
	ctx["masonary_ideas"] = current_page 
	template_file = "usermgmt/account_dashboard.html"
	return render(request,template_file,ctx)

@login_required
def account_notification_page(request,page_num):
	ctx = {}
	ctx["date"] = Date()
	ctx["page_num"] = page_num
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	# Split data into pages
	notifications = Paginator(profile.notification.all().order_by("-pk"),NOTIFICATION_PER_PAGE)
	ctx["max_page"] = notifications.num_pages
	try: current_page = notifications.page(page_num) # Get the ideas on the current page
	except: raise Http404()
	ctx["notifications"] = current_page 

	# Count new notifications
	ctx["new_notification"] = profile.notification.filter(dismissed=False).count()
	
	# Dismiss notifications on THIS PAGE
	ctx["undismissed_notifications"] = []
	for notification in current_page:
		if not notification.dismissed:
			ctx["undismissed_notifications"].append(notification)
			notification.dismissed = True
			notification.save()

	template_file = "usermgmt/account_notification.html"
	return render(request,template_file,ctx)

@login_required
def account_follow_view(request,username):
	target_profile = get_object_or_404(
		Profile,
		user=get_object_or_404(User,username=username,is_active=True)
	)
	profile = get_object_or_404(Profile,user=request.user)
	# Check if the current user is blocked by the target user
	if target_profile.blocked_user.filter(username=request.user.username).exists():
		absolute_url = request.build_absolute_uri(reverse('account_dashboard_page', args=(username,'my',1)))
		message = f"<a href='{absolute_url}'>@{username}</a> has blocked you, you cannot follow this user"
		msg = Notification.objects.create(message=message,message_status=1)
		msg.save()
		profile.notification.add(msg)
	else:
		# Check whether the current user is already following the target user
		if profile.following.filter(username=username).exists():
			profile.following.remove(target_profile.user)
		else:
			profile.following.add(target_profile.user)
	profile.save()
	return redirect("account_dashboard_page",username=username,content_filter="my",page_num=1)

@login_required
def account_people_page(request,username,follower_page_num,following_page_num):
	ctx = {}
	ctx["date"] = Date()
	user = get_object_or_404(User,username=username)
	ctx["profile"] = profile = get_object_or_404(Profile,user=user)

	# Blocked users can't see this page
	if request.user == profile.user or not profile.blocked_user.filter(username=request.user.username).exists():
		ctx["username"] = username
		ctx["follower_page_num"] = follower_page_num
		ctx["following_page_num"] = following_page_num

		# Get followers
		followers = User.objects.filter(profile__following=user) # User obj
		followers = Profile.objects.filter(user__in=followers).order_by("-timestamp") # Profile obj	
		# Split data into pages
		followers = Paginator(followers,USER_PER_PAGE)
		ctx["follower_max_page"] = followers.num_pages
		try: current_page = followers.page(follower_page_num) # Get the ideas on the current page
		except: raise Http404()
		ctx["followers"] = current_page

		# Get following user
		# Split data into pages
		followings = Profile.objects.filter(user__in=profile.following.all()).order_by("-timestamp")
		followings = Paginator(followings,USER_PER_PAGE)
		ctx["following_max_page"] = followings.num_pages
		try: current_page = followings.page(following_page_num) # Get the ideas on the current page
		except: raise Http404()
		ctx["followings"] = current_page  
	else:
		return redirect("access_error_page")

	template_file = "usermgmt/account_people.html"
	return render(request,template_file,ctx)

RESULT_PER_PAGE = 20

@login_required
def account_meet_page(request,page_num,username):
	ctx = {}
	ctx["date"] = date = Date()
	ctx["page_num"] = page_num
	if username == "None":
		username = request.GET.get('username',None)
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	today = date.now()
	current_date = int_date(f"{today.strftime('%Y')}-{date.week()}-1")
	timestamp_from = current_week_dates(*current_date)
	timestamp_to = timestamp_from + datetime.timedelta(days=7)

	# Find random users created within the past 6 months
	random_profiles = Profile.objects.filter(
		timestamp__gte = date.now() - datetime.timedelta(days=182),
		timestamp__lte = date.now() + datetime.timedelta(days=1),
		user__is_active = True,
	).distinct().exclude(user=profile.user).exclude(discover_setting=1)
	ctx["random_profiles"] = random.sample(list(random_profiles), min(random_profiles.count(), 20))

	# Find users with the same interest (same favourite tags)
	like_minded_profiles = Profile.objects.filter(
		tags__in=profile.tags.all(),
		user__is_active = True,
	).distinct().exclude(user=profile.user).exclude(discover_setting=1)
	ctx["like_minded_profiles"] = random.sample(list(like_minded_profiles), min(like_minded_profiles.count(), 20))

	# People followed by people that you follow
	followings = random.sample(list(profile.following.all()), min(profile.following.count(), 10))
	followings = Profile.objects.filter(user__in=followings)
	close_profiles = []
	for following_profile in followings:
		# Find 3 random users followed by people that you follow
		users = random.sample(list(following_profile.following.all()), min(following_profile.following.count(), 3))
		users = Profile.objects.filter(user__in=users,user__is_active=True).exclude(discover_setting=1)
		close_profiles = close_profiles + list(set(users) - set(close_profiles))
	
	# Remove yourself from list
	if profile in close_profiles:
		close_profiles.remove(profile)
	ctx["close_profiles"] = close_profiles

	if username:
		ctx["username"] = username
		users = User.objects.filter(username__icontains=username,is_active=True)
		if not users:
			ctx["error"] = SERVER_ERROR["AUTH_NO_USER"]
		else:
			if users.count() > 1: # If there are more than 1 results
				search_results = Profile.objects.filter(user__in=users)
				ctx["entry_count"] = search_results.count()
				search_results = Paginator(search_results,RESULT_PER_PAGE)
				ctx["max_page"] = search_results.num_pages
				try: current_page = search_results.page(page_num) # Get the ideas on the current page
				except: raise Http404()
				ctx["search_results"] = current_page 
			else:
				user = users.first()
				ctx["search_profile"] = search_profile = get_object_or_404(Profile, user=user)
				recent_ideas = Idea.objects.filter(author=search_profile).order_by("-timestamp")
				# Remove private ideas if searched user is not the current user
				if profile != search_profile:
					recent_ideas = recent_ideas.exclude(publish_status=1)
				# Remove follower only ideas if searched user is not followed by the current user
				if not profile.following.filter(username=search_profile.user.username).exists():
					recent_ideas = recent_ideas.exclude(publish_status=2)
				if recent_ideas.count() > 4:
					ctx["more_ideas"] = True
				ctx["recent_ideas"] = recent_ideas[:4]
				# The total number of public ideas(posts) created by this user
				ctx["idea_count"] = Idea.objects.filter(author=search_profile,publish_status=3).order_by("-timestamp").count()

	template_file = "usermgmt/account_meet.html"
	return render(request,template_file,ctx)

