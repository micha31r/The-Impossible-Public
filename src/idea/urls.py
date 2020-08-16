from django.urls import path

from .views import (
	# Idea
	explore_page,
	feed_page,
	detail_page,
	create_view,
	limit_page,
	edit_page,
	search_page,
	# Like and star
	like_view,
	star_view,
	# Comment
	comment_delete_view,
	comment_get_view
)

urlpatterns = [
	# Idea
	path('explore/<int:week_num>/<int:page_num>', explore_page, name="idea_explore_page"),
	path('feed', feed_page, name="idea_feed_page"),
	path('detail/<int:pk>', detail_page, name="idea_detail_page"),
	path('create', create_view, name="idea_create_view"),
	path('limit', limit_page, name="idea_limit_page"),
	path('edit/<int:pk>', edit_page, name="idea_edit_page"),
	path('search/<int:page_num>/<slug:name>', search_page, name="idea_search_page"),

	# Like and star
	path('like', like_view, name="idea_like_view"),
	path('star', star_view, name="idea_star_view"),

	# Comment
	path('comment/delete/<int:comment_pk>/<int:idea_pk>', comment_delete_view, name="idea_comment_delete_view"),
	path('comment/get', comment_get_view, name="idea_comment_get_view"),
] 