from django.db import models
from usermgmt.models import Profile

PUBLISH_OPTION = (
	(1,"Private"), # For individual users
    (2,"Public"), # For the whole world (all users) !! Beware !!
)

class Feedback(models.Model):
	author = models.ForeignKey(
	    Profile,
	    on_delete=models.CASCADE,
	)
	description = models.TextField(max_length=1000, blank=False)
	viewed = models.BooleanField(default=False)
	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.description[:100]

class Question(models.Model):
	author = models.ForeignKey(
	    Profile,
	    on_delete=models.CASCADE,
	)
	short_description = models.CharField(max_length=150, blank=False)
	description = models.TextField(max_length=1000, blank=False)
	solved = models.BooleanField(default=False)
	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.short_description[:100]

class CoreFeed(models.Model):
	name = models.CharField(max_length=500, blank=False)
	description = models.TextField(max_length=2000, blank=False)
	publish_status = models.IntegerField(default=1,choices=PUBLISH_OPTION)
	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.name

