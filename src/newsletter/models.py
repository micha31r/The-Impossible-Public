import string, random
from django.db import models
from django.utils import timezone

FREQUENCY_OPTION = (
	(1,"Never"),
    (2,"Weekly"),
    (3,"Monthly"),
)

def slug_generator(seed,size=20, chars=string.ascii_uppercase + string.digits):
	random.seed(seed)
	return ''.join(random.choice(chars) for _ in range(size))

class Subscriber(models.Model):

	email = models.EmailField(max_length=250)
	frequency = models.IntegerField(default=2,choices=FREQUENCY_OPTION)
	slug = models.SlugField(blank=True)

	def save(self, *args, **kwargs):
		self.slug = slug_generator(self.id)
		super().save(*args, **kwargs)

	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True)
	last_sent = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.email


