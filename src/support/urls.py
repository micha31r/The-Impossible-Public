from django.urls import path

from .views import (
	feedback_page,
	question_page,
)

urlpatterns = [
	path('feedback', feedback_page, name="support_feedback_page"),
	path('question', question_page, name="support_question_page"),
]
