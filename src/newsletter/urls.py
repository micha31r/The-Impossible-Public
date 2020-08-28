from django.urls import path
from django.conf import settings

from .views import (
	join_view,
	unenroll_page,
	email_page,
)

app_name = 'newsletter'

urlpatterns = [
	path('join/', join_view, name="join_view"),
	path('unenroll/<slug:slug>', unenroll_page, name="unenroll_page"),
] 

if settings.DEBUG:
	# THIS IS FOR TESTING ONLY !!
	urlpatterns.append(path('email', email_page, name="email_page"))