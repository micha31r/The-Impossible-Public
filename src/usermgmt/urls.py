from django.urls import path
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from .sitemaps import ProfileSitemap

from .views import (
	signup_page,
	verify_page,
	send_code_view,
	email_page,
	login_page,
	logout_page,
	logout_view,
	account_dashboard_page,
	account_notification_page,
	account_follow_view,
	account_people_page,
	account_meet_page,
)

from .setting_views import (
	account_setting_profile_page,
	account_setting_password_page,
	account_setting_explore_content_page,
	account_setting_notification_page,
	account_setting_privacy_page,
	account_setting_newsletter_page,
)

sitemaps = {
    'profiles': ProfileSitemap
}

app_name = 'usermgmt'

urlpatterns = [
	# Site map 
	path('sitemap.xml', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),

	path('signup', signup_page, name="signup_page"),
	path('verify/<slug:username>', verify_page, name="verify_page"),
	path('send-code/<slug:username>', send_code_view, name="send_code_view"),
	path('login', login_page, name="login_page"),
	path('logout', logout_page, name="logout_page"),
	path('logout/comfirmed', logout_view, name="logout_view"),
	path('account/dashboard/<slug:username>/<str:content_filter>/<int:page_num>', account_dashboard_page, name="account_dashboard_page"),
	path('account/notification/<int:page_num>/', account_notification_page, name="account_notification_page"),
	path('account/follow/<slug:username>/', account_follow_view, name="account_follow_view"),
	path('account/people/<slug:username>/<int:follower_page_num>/<int:following_page_num>', account_people_page, name="account_people_page"),
	path('account/meet/<int:page_num>/<slug:username>', account_meet_page, name="account_meet_page"),
	
	# Account settings
	path('account/settings/profile', account_setting_profile_page, name="account_setting_profile_page"),
	path('account/settings/password', account_setting_password_page, name="account_setting_password_page"),
	path('account/settings/explore-content', account_setting_explore_content_page, name="account_setting_explore_content_page"),
	path('account/settings/notification', account_setting_notification_page, name="account_setting_notification_page"),
	path('account/settings/privacy', account_setting_privacy_page, name="account_setting_privacy_page"),
	path('account/settings/newsletter', account_setting_newsletter_page, name="account_setting_newsletter_page"),
]

if settings.DEBUG:
	# THIS IS FOR TESTING ONLY !!
	urlpatterns.append(path('email', email_page, name="email_page"))
