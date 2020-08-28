from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from userupload.models import (
	File,
	slug_generator
)

User = settings.AUTH_USER_MODEL

PUBLISH_OPTION = (
	(1,"Private"),
    (2,"Public"),
)

LIKE_OPTION = (
	(1,"Off"),
    (2,"From Followers"),
    (3,"From Everyone"),
)

COMMENT_OPTION = (
	(1,"Off"),
    (2,"From Followers"),
    (3,"From Everyone"),
)

DISCOVER_OPTION = (
	(1,"Hide"),
    (2,"Discoverable"),
)

USE_TAG_FILTER_OPTION = (
	(1,"Filter Off"),
    (2,"Filter On"),
)

class Notification(models.Model):
	# If this is too short then it may result in HTML error
	message = models.CharField(max_length=1000)
	message_status = models.IntegerField(default=1,choices=PUBLISH_OPTION)
	dismissed = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True) # default=timezone.now

	def __str__(self):
		return self.message[:50] + '...' 

class Verification(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
	slug = models.SlugField(max_length=6,blank=True)
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slug_generator(self.id,size=6)
		super(Verification, self).save(*args, **kwargs)

class Profile(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

	profile_img = models.ForeignKey(File,on_delete=models.SET_NULL,blank=True,null=True)
	bio = models.TextField(max_length=160,blank=True,unique=False)
	website = models.URLField(max_length=160,blank=True,unique=False)
	location = models.CharField(max_length=50,blank=True,null=True)
	following = models.ManyToManyField(User,blank=True,related_name="following")
	notification = models.ManyToManyField(Notification,blank=True,related_name="notification")
	tags = models.ManyToManyField("idea.Tag",blank=True,related_name="fav_tags")
	blocked_user = models.ManyToManyField(User,blank=True,related_name="blocked")
	
	core_feed = models.ManyToManyField("support.CoreFeed",blank=True,related_name="core_feed")
	subscriber = models.ForeignKey("newsletter.Subscriber",on_delete=models.SET_NULL,blank=True,null=True)

	# Whether to the user's favourite tags as content filter in explore
	use_tag_filter = models.IntegerField(default=1,choices=USE_TAG_FILTER_OPTION)

	# Social settings
	like_setting = models.IntegerField(default=3,choices=LIKE_OPTION)
	comment_setting = models.IntegerField(default=3,choices=COMMENT_OPTION)

	# Allow others to see this user in Discover People Page
	discover_setting = models.IntegerField(default=2,choices=DISCOVER_OPTION)

    # Only allow each user to post 5 ideas per day
	daily_limit = models.IntegerField(default=5)
	daily_limit_timestamp = models.DateTimeField(default=timezone.now)

	timestamp = models.DateTimeField(auto_now_add=True) # default=timezone.now

	def get_absolute_url(self):
		return reverse('usermgmt:account_dashboard_page', args=(self.user.username,"my",1))

	def __str__(self):
		full_name = "Anonymous"
		try: full_name = self.user.get_full_name() 
		except: pass
		return full_name 