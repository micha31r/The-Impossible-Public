# This file is for all account settings related views

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django import forms

from .models import Profile, Notification

from .forms import (
	ProfileForm,
	PasswordForm,
	ExploreContentForm,
	NotificationForm,
	PrivacyForm,
)

from newsletter.models import Subscriber

from newsletter.forms import NewsletterForm

from userupload.models import File

from idea.models import Tag

from idea.utils import at_filter

from the_impossible.utils import *

from the_impossible.ERROR import *

@login_required
def account_setting_profile_page(request):
	ctx = {}
	ctx["date"] = Date()
	profile = get_object_or_404(Profile,user=request.user)

	# User Profile Form
	initial = {
		"first_name":profile.user.first_name,
		"last_name":profile.user.last_name,
		"email":profile.user.email,
		"bio":profile.bio,
		"website":profile.website,
		"location":profile.location,
	}
	form = ProfileForm(request.POST or None, initial=initial)
	ctx["form"] = form

	if form.is_valid():
		profile.user.first_name = form.cleaned_data.get("first_name").capitalize()
		profile.user.last_name = form.cleaned_data.get("last_name").capitalize()
		profile.user.email = form.cleaned_data.get("email")
		profile.bio = form.cleaned_data.get("bio")
		profile.website = form.cleaned_data.get("website")
		profile.location = form.cleaned_data.get("location")
		profile.user.save()
		profile.save()

	ctx["form_template_page"]="usermgmt/account_setting_profile.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)

@login_required
def account_setting_password_page(request):
	ctx = {}
	ctx["date"] = Date()
	profile = get_object_or_404(Profile,user=request.user)

	# Reset Password Form
	ctx["form"] = form = PasswordForm(request.POST or None)
	if form.is_valid():
		current_passsword = form.cleaned_data.get("current_password")
		new_password = form.cleaned_data.get("new_password")
		user = authenticate(request, username=request.user.username, password=current_passsword)
		if user:
			if new_password == form.cleaned_data.get("password_confirmation"):
				user.set_password(new_password)
				user.save()
		else:
			ctx["error"] = SERVER_ERROR["AUTH_PASSWORD"]

	ctx["form_template_page"]="usermgmt/account_setting_password.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)

@login_required
def account_setting_explore_content_page(request):
	ctx = {}
	ctx["date"] = Date()
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	ctx["form"] = form = ExploreContentForm(request.POST or None)
	form.fields["tags"].queryset = profile.tags

	# Show avaliable tags
	qs = Tag.objects.all().distinct()
	for tag in profile.tags.all():
		qs = qs.exclude(name=tag.name)
	ctx["tags"] = qs

	form.fields["tags_remain"].widget = forms.SelectMultiple(choices=[(choice.id, choice) for choice in qs])
	form.fields["use_tag_filter"].initial = profile.use_tag_filter

	if form.is_valid():
		data = form.cleaned_data
		# Add tags
		for tag in eval(data.get('tags_remain') or "[]"): # convert
			profile.tags.add(tag)

		# Remove tags
		for tag in data.get('tags'):
			profile.tags.remove(tag)

		profile.use_tag_filter = 1
		if profile.tags.count() > 0:
			profile.use_tag_filter = data.get("use_tag_filter")

		profile.save()

	ctx["form_template_page"]="usermgmt/account_setting_explore_content.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)

@login_required
def account_setting_notification_page(request):
	ctx = {}
	ctx["date"] = Date()
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	ctx["form"] = form = NotificationForm(request.POST or None)
	form.fields["like_setting"].initial = profile.like_setting
	form.fields["comment_setting"].initial = profile.comment_setting

	if form.is_valid():
		data = form.cleaned_data
		profile.like_setting = data.get("like_setting")
		profile.comment_setting = data.get("comment_setting")
		profile.save()

	ctx["form_template_page"]="usermgmt/account_setting_notification.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)

@login_required
def account_setting_privacy_page(request):
	ctx = {}
	ctx["date"] = Date()
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	ctx["form"] = form = PrivacyForm(request.POST or None)
	form.fields["discover_setting"].initial = profile.discover_setting

	usernames_before_edit = ""
	for user in profile.blocked_user.all():
		usernames_before_edit += f"@{user.username} "
	form.fields["blocked_user"].initial = usernames_before_edit

	if form.is_valid():
		data = form.cleaned_data
		profile.discover_setting = data.get("discover_setting")
		
		# Search description for @ users
		usernames = set(at_filter(data.get("blocked_user"))) - set(usernames_before_edit)
		
		# Remove blocked users
		for user in profile.blocked_user.all():
			if user.username not in at_filter(data.get("blocked_user")):
				profile.blocked_user.remove(user)

		# Add blocked users
		for username in usernames:
			user = User.objects.filter(username=username).first()
			if user:
				# Add user to blocked user
				profile.blocked_user.add(user)
			else: 
				# Tell the current user that their mentioned user does not exist
				profile = get_object_or_404(Profile,user=request.user)
				message = f"@{username} user does not exist"
				msg = Notification.objects.create(message=message,message_status=1)
				msg.save()
				profile.notification.add(msg)
				ctx["error"] = f"@{username} {SERVER_ERROR['AUTH_NO_USER']}"
		
		profile.save()

		# Remove current followers thats blocked
		followers = User.objects.filter(profile__following=profile.user)
		for follower in followers:
			if profile.blocked_user.filter(username=follower.username).exists():
				target_profile = get_object_or_404(Profile,user=follower)
				target_profile.following.remove(profile.user)
				# Send blocked message to the blocked user
				absolute_url = request.build_absolute_uri(reverse('account_dashboard_page', args=(profile.user.username,'my',1)))
				message = f"@<a href='{absolute_url}'>{profile.user.username}</a> has blocked you. You can no longer see the user's follower-only posts"
				msg = Notification.objects.create(message=message,message_status=1)
				msg.save()
				target_profile.notification.add(msg)
				target_profile.save()

	ctx["form_template_page"]="usermgmt/account_setting_privacy.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)

@login_required
def account_setting_newsletter_page(request):
	ctx = {}
	ctx["date"] = Date()
	ctx["profile"] = profile = get_object_or_404(Profile,user=request.user)

	if not profile.subscriber:
		obj = Subscriber.objects.filter(email=request.user.email).first()
		if not obj:
			obj = Subscriber.objects.create(email=request.user.email)
			obj.save()
		profile.subscriber = obj
		profile.save()

	ctx["form"] = form = NewsletterForm(request.POST or None)
	form.fields["email"].initial = profile.subscriber.email
	form.fields["frequency"].initial = profile.subscriber.frequency

	if form.is_valid():
		profile.subscriber.email = form.cleaned_data.get("email")
		profile.subscriber.frequency = form.cleaned_data.get("frequency")
		profile.subscriber.save()

	ctx["form_template_page"]="usermgmt/account_setting_newsletter.html"
	template_file = "usermgmt/account_setting.html"
	return render(request,template_file,ctx)


