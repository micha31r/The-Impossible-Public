from django.urls import path

from .views import (
	idea_img_page,
	idea_img_delete_page,
	profile_img_page,
	profile_img_delete_page,
)

urlpatterns = [
	path('file/idea/<int:idea_pk>/<slug:file_pk>/<str:field>', idea_img_page, name="userupload_idea_img_page"),
	path('file/delete/idea/<slug:redirect_name>/<int:obj_pk>/<slug:file_pk>/', idea_img_delete_page, name="userupload_idea_img_delete_page"),

	path('file/profile/<int:profile_pk>/<slug:file_pk>/', profile_img_page, name="userupload_profile_img_page"),
	path('file/delete/profile/<slug:redirect_name>/<slug:username>/<str:content_filter>/<int:page_num>/<slug:file_pk>/', profile_img_delete_page, name="userupload_profile_img_delete_page"),
] 