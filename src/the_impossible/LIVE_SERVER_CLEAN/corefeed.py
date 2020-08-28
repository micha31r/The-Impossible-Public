# Deletes all corefeed

from support.models import CoreFeed

CoreFeed.objects.all().delete()

