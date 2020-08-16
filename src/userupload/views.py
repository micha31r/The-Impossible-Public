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
def idea_img_page(request,idea_pk,file_pk,field):
	ctx = {} # Context variables
	ctx["date"] = Date()
	# file_pk can be an integer or None
	ctx["file"] = file = File.objects.filter(pk=file_pk.isdigit() and file_pk or -1).first()
	ctx["form"] = form = FileForm(request.POST or None, request.FILES or None)
	ctx["redirect_name"] = redirect_name = "idea_edit_page"

	ctx["obj"] = idea = get_object_or_404(Idea, pk=idea_pk)

	if idea.author.user == request.user:
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
						file.file = uploaded_file
						file.save()
					file.save()

					# Link file to parent object
					if field == "header":
						idea.header_img = file
					elif field == "body":
						idea.body_img.add(file)
					idea.save()
					return redirect(redirect_name,pk=idea_pk)

				# Invalid file type
				else:
					ctx["error"] = SERVER_ERROR["FILE"]
			# If user didn't replace the old file
			elif file.file:
				# This only work if the url name starts with the model's name. E.G: idea_edit_page
				return redirect(redirect_name,pk=idea_pk)
	else:
		return redirect("access_error_page")
	template_file = "userupload/idea_img.html"
	return render(request,template_file,ctx)

@login_required
def idea_img_delete_page(request,redirect_name,obj_pk,file_pk):
	file = get_object_or_404(File, pk=file_pk)
	file.delete()
	return redirect(redirect_name,pk=obj_pk)

@login_required
def profile_img_page(request,profile_pk,file_pk):
	ctx = {} # Context variables
	ctx["date"] = Date()
	# file_pk can be an integer or None
	ctx["file"] = file = File.objects.filter(pk=file_pk.isdigit() and file_pk or -1).first()
	ctx["form"] = form = FileForm(request.POST or None, request.FILES or None)
	ctx["redirect_name"] = redirect_name = "account_dashboard_page"

	ctx["obj"] = profile = get_object_or_404(Profile, pk=profile_pk)

	if profile.user == request.user:
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
						file.file = uploaded_file
						file.save()
					file.save()

					# Link file to parent object
					profile.profile_img = file
					profile.save()
					return redirect(redirect_name,username=request.user.username,content_filter="my",page_num=1)

				# Invalid file type
				else:
					ctx["error"] = SERVER_ERROR["FILE"]
			# If user didn't replace the old file
			elif file.file:
				# This only work if the url name starts with the model's name. E.G: idea_edit_page
				return redirect(redirect_name,username=request.user.username,content_filter="my",page_num=1)
	else:
		return redirect("access_error_page")
	template_file = "userupload/profile_img.html"
	return render(request,template_file,ctx)
	
@login_required
def profile_img_delete_page(request,redirect_name,username,content_filter,page_num,file_pk):
	file = get_object_or_404(File, pk=file_pk)
	file.delete()
	return redirect(redirect_name,username=username,content_filter=content_filter,page_num=page_num)


