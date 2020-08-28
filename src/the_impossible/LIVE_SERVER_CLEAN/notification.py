# Deletes all notifications

from usermgmt.models import Notification

Notification.objects.all().delete()

