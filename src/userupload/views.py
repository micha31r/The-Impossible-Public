import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *

from idea.models import Idea

from usermgmt.models import Profile

from the_impossible.utils import *

from the_impossible.ERROR import *

from .utils import *

from .forms import (
	FileForm
)

@login_required
def idea_header_img_page(request,idea_pk):
	ctx = {} # Context variables
	ctx["date"] = Date()
	ctx["obj"] = idea = get_object_or_404(Idea, pk=idea_pk, author__user=request.user)
	ctx["file"] = file = idea.header_img
	ctx["form"] = form = FileForm(request.POST or None, request.FILES or None)

	# If there is an exsisting file object
	if file:
		# Set default values
		form.fields["description"].initial = file.description
		form.fields["file"].initial = file.file

	if form.is_valid():
		uploaded_file = request.FILES.get("file")
		if uploaded_file:
			if file_is_valid(uploaded_file.name,"image"):	
				data = form.cleaned_data

				# Create file
				if not file:
					file = File.objects.create(
						user=request.user,
						description = data.get("description"),
						file = uploaded_file
					)
				else: # replace file
					file.description = form.cleaned_data.get("description")

					# Delete the old file
					if os.path.isfile(file.file.path):
						os.remove(file.file.path)

					file.file = uploaded_file
					file.save()
				file.save()

				# Link file to parent object
				idea.header_img = file
				idea.save()
				return redirect(f"idea:edit_page",pk=idea_pk)

			# Invalid file type
			else:
				ctx["error"] = SERVER_ERROR["FILE"]
		# If user didn't replace the old file
		elif file.file:
			# This only work if the url name starts with the model's name. E.G: idea_edit_page
			return redirect(f"idea:edit_page",pk=idea_pk)
	template_file = "userupload/idea_header_img.html"
	return render(request,template_file,ctx)

@login_required
def idea_header_img_delete_page(request,idea_pk):
	idea = get_object_or_404(Idea, pk=idea_pk, author__user=request.user)
	# Make sure the user has access before deleting the file
	if idea.header_img:
		idea.header_img.delete()
	return redirect(f"idea:edit_page",pk=idea_pk)

@login_required
def idea_body_img_page(request,idea_pk,file_pk):
	ctx = {} # Context variables
	ctx["date"] = Date()

	ctx["obj"] = idea = get_object_or_404(Idea, pk=idea_pk, author__user=request.user)
	file = None
	if file_pk != "None":
		file = get_object_or_404(idea.body_img,pk=file_pk)
	ctx["file"] = file
	ctx["form"] = form = FileForm(request.POST or None, request.FILES or None)

	# If there is an exsisting file object
	if file:
		# Set default values
		form.fields["description"].initial = file.description
		form.fields["file"].initial = file.file

	if form.is_valid():
		uploaded_file = request.FILES.get("file")
		if uploaded_file:
			if file_is_valid(uploaded_file.name,"image"):	
				data = form.cleaned_data

				# Create file
				if not file:
					file = File.objects.create(
						user=request.user,
						description = data.get("description"),
						file = uploaded_file
					)
				else: # replace file
					file.description = form.cleaned_data.get("description")

					# Delete the old file
					if os.path.isfile(file.file.path):
						os.remove(file.file.path)

					file.file = uploaded_file
					file.save()
				file.save()

				# Link file to parent object
				idea.body_img.add(file)
				idea.save()
				return redirect(f"idea:edit_page",pk=idea_pk)

			# Invalid file type
			else:
				ctx["error"] = SERVER_ERROR["FILE"]
		# If user didn't replace the old file
		elif file.file:
			# This only work if the url name starts with the model's name. E.G: idea_edit_page
			return redirect(f"idea:edit_page",pk=idea_pk)
	template_file = "userupload/idea_body_img.html"
	return render(request,template_file,ctx)

@login_required
def idea_body_img_delete_page(request,idea_pk,file_pk):
	idea = get_object_or_404(Idea, pk=idea_pk, author__user=request.user)
	# Make sure the user has access before deleting the file
	if idea.body_img.filter(pk=file_pk).exists():
		idea.body_img.filter(pk=file_pk).delete()
	return redirect(f"idea:edit_page",pk=idea_pk)

@login_required
def profile_img_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	ctx["obj"] = profile = get_object_or_404(Profile, user=request.user)
	ctx["file"] = file = profile.profile_img
	ctx["form"] = form = FileForm(request.POST or None, request.FILES or None)

	# If there is an exsisting file object
	if file:
		# Set default values
		form.fields["description"].initial = file.description
		form.fields["file"].initial = file.file

	if form.is_valid():
		uploaded_file = request.FILES.get("file")
		if uploaded_file:
			if file_is_valid(uploaded_file.name,"image"):	
				data = form.cleaned_data

				# Create file
				if not file:
					file = File.objects.create(
						user=request.user,
						description = data.get("description"),
						file = uploaded_file
					)
				else: # replace file
					file.description = form.cleaned_data.get("description")

					# Delete the old file
					if os.path.isfile(file.file.path):
						os.remove(file.file.path)
					
					file.file = uploaded_file
					file.save()
				file.save()

				# Link file to parent object
				profile.profile_img = file
				profile.save()
				return redirect(f"usermgmt:account_dashboard_page",username=request.user.username,content_filter="my",page_num=1)

			# Invalid file type
			else:
				ctx["error"] = SERVER_ERROR["FILE"]
		# If user didn't replace the old file
		elif file.file:
			# This only work if the url name starts with the model's name. E.G: idea_edit_page
			return redirect(f"usermgmt:account_dashboard_page",username=request.user.username,content_filter="my",page_num=1)
	template_file = "userupload/profile_img.html"
	return render(request,template_file,ctx)
	
@login_required
def profile_img_delete_page(request):
	profile = get_object_or_404(Profile,user=request.user)
	if profile.profile_img:
		profile.profile_img.delete()
	return redirect(f"usermgmt:account_dashboard_page",username=request.user.username,content_filter="my",page_num=1)


