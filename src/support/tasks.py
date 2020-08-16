from django.conf import settings
from background_task import background
from templated_email import send_templated_mail

@background(schedule=20)
def support_email(email,username,question_id):
    send_templated_mail(
        template_name='question',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        context={
            'username':username,
            'question_id':question_id,
        },
	)