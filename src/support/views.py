from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Feedback, Question

from .forms import (
	FeedbackForm,
	QuestionForm,
)

from .tasks import support_email

from the_impossible.utils import *

from usermgmt.models import Profile

@login_required
def feedback_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	profile = get_object_or_404(Profile,user=request.user)
	form = FeedbackForm(request.POST or None)
	ctx["form"] = form
	if form.is_valid():
		obj = Feedback.objects.create(
			author=profile,
			description=form.cleaned_data.get("description")
		)
		obj.save()
		ctx["success"] = True
	template_file = "support/feedback.html"
	return render(request,template_file,ctx)

@login_required
def question_page(request):
	ctx = {} # Context variables
	ctx["date"] = Date()
	profile = get_object_or_404(Profile,user=request.user)
	form = QuestionForm(request.POST or None)
	ctx["form"] = form
	if form.is_valid():
		obj = Question.objects.create(
			author=profile,
			short_description=form.cleaned_data.get("short_description"),
			description=form.cleaned_data.get("description")
		)
		obj.save()
		ctx["question_id"] = obj.id

		support_email(
			email=request.user.email,
			username=request.user.username,
			question_id=obj.id
		)

	template_file = "support/question.html"
	return render(request,template_file,ctx)
