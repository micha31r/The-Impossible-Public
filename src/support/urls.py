from django.urls import path

from .views import (
	feedback_page,
	question_page,
)

app_name = 'support'

urlpatterns = [
	path('feedback', feedback_page, name="feedback_page"),
	path('question', question_page, name="question_page"),
]
