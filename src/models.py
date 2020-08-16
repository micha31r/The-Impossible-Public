from django.db import models
from django.utils import timezone
from django.conf import settings

from usermgmt.models import (
	Profile,
)

from userupload.models import File

User = settings.AUTH_USER_MODEL

PUBLISH_OPTION = (
	(1,"Draft"),
    (2,"Followers only"),
    (3,"Public"),
)

class Tag(models.Model):
	class Meta:
		ordering = ['name']

	name = models.CharField(max_length=100, blank=False, unique=True)

	def __str__(self):
		return self.name

# Once posted the comment can be deleted but not edited.
class Comment(models.Model):
	author = models.ForeignKey(
		Profile,
		on_delete=models.CASCADE
	)

    # Content
	full_description = models.TextField(max_length=280,blank=False,unique=False)
	
	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) # default=timezone.now
	last_edit = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.full_description[:50] + '...' 

class Idea(models.Model):

	# Order data by name
	class Meta:
		ordering = ['-id']

	# Settings
	author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
	publish_status = models.IntegerField(default=1,choices=PUBLISH_OPTION)
	tags = models.ManyToManyField(Tag,related_name="tagged",blank=True)

    # Content
	header_img = models.ForeignKey(File,on_delete=models.SET_NULL,blank=True,null=True)
	body_img = models.ManyToManyField(File,related_name="body_image",blank=True)

	name = models.CharField(max_length=70,blank=False,unique=False)
	short_description = models.TextField(max_length=150,blank=False,unique=False)
	full_description = models.TextField(max_length=1000,blank=False,unique=False)
	
	# Likes and views
	viewed_user = models.ManyToManyField(Profile,related_name="viewed",blank=True)
	liked_user = models.ManyToManyField(Profile,related_name="liked",blank=True)
	starred_user = models.ManyToManyField(Profile,related_name="starred",blank=True)
	
	# Comments
	comments = models.ManyToManyField(Comment,related_name="comment",blank=True)

	# Notification to followers
	notified = models.BooleanField(default=False)

	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) # default=timezone.now
	last_edit = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
