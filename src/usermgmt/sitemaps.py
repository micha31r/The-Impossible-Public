from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import Length
from django.urls import reverse

from .models import Profile

from the_impossible.utils import Date

# class StaticSitemap(Sitemap):
# 	changefreq = "yearly"
# 	priority = 0.5

# 	def items(self):
# 		return [
# 			'usermgmt:login_page',
# 			'usermgmt:signup_page',
# 			'usermgmt:account_meet_page',
# 		]

# 	def location(self, item):
# 		date = Date()
# 		args = {
# 			'usermgmt:login_page':None,
# 			'usermgmt:signup_page':None,
# 			'usermgmt:account_meet_page':(1,None),
# 		}
# 		return reverse(item, args=args[item])

class ProfileSitemap(Sitemap):    
	changefreq = "daily"
	priority = 0.2

	def items(self):
		# Retrieve the most popular users
		qs = Profile.objects.annotate(follower_count=Count('user__profile__user__following')).filter(user__is_active=True).order_by('-follower_count')[:10000]
		return qs

