# Deletes all Feedbacks

from usermgmt.models import Feedback

Feedback.objects.all().delete()

