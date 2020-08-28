from django.urls import path
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticSitemap

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

sitemaps = {
	'static': StaticSitemap
}

app_name = 'idea'

urlpatterns = [
	# Site map 
	path('sitemap.xml', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),

	# Idea
	path('explore/<int:week_num>/<int:page_num>', explore_page, name="explore_page"),
	path('feed', feed_page, name="feed_page"),
	path('detail/<int:pk>', detail_page, name="detail_page"),
	path('create', create_view, name="create_view"),
	path('limit', limit_page, name="limit_page"),
	path('edit/<int:pk>', edit_page, name="edit_page"),
	path('search/<int:page_num>/<slug:name>', search_page, name="search_page"),

	# Like and star
	path('like', like_view, name="like_view"),
	path('star', star_view, name="star_view"),

	# Comment
	path('comment/delete/<int:comment_pk>/<int:idea_pk>', comment_delete_view, name="comment_delete_view"),
	path('comment/get', comment_get_view, name="comment_get_view"),
] 