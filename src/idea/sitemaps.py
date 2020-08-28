from django.contrib.sitemaps import Sitemap
from django.db.models import Count
from django.db.models.functions import Length
from django.urls import reverse

from .models import Idea

from the_impossible.utils import Date

class StaticSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.8

	def items(self):
		return [
			'idea:explore_page',
		]

	def location(self, item):
		date = Date()
		args = {
			'idea:explore_page':(date.week(),1),
		}
		return reverse(item, args=args[item])

# class IdeaSitemap(Sitemap):    
# 	changefreq = "weekly"
# 	priority = 0.6

# 	def items(self):
# 		# Return the top 1000 most viewed ideas - with a reasonable amount of words
# 		qs = Idea.objects.annotate(view_count=Count('viewed_user'),text_length=Length('full_description')).filter(publish_status=3,text_length__gte=500).order_by('-view_count')[:10000]
# 		return qs

# 	# Last edited
# 	def lastmod(self, obj):
# 		return obj.last_edit