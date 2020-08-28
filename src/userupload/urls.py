from django.urls import path

from .views import (
	idea_header_img_page,
	idea_body_img_page,
	idea_header_img_delete_page,
	idea_body_img_delete_page,
	profile_img_page,
	profile_img_delete_page,
)

app_name = 'userupload'

urlpatterns = [
	path('file/idea/header/<int:idea_pk>', idea_header_img_page, name="idea_header_img_page"),
	path('file/delete/idea/<int:idea_pk>', idea_header_img_delete_page, name="idea_header_img_delete_page"),
	path('file/idea/body/<int:idea_pk>/<slug:file_pk>', idea_body_img_page, name="idea_body_img_page"),
	path('file/delete/idea/<int:idea_pk>/<slug:file_pk>', idea_body_img_delete_page, name="idea_body_img_delete_page"),

	path('file/profile', profile_img_page, name="profile_img_page"),
	path('file/delete/profile', profile_img_delete_page, name="profile_img_delete_page"),
] 