# Deletes all Questions

from usermgmt.models import Question

Question.objects.all().delete()

