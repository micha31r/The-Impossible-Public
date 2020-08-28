from django.core.mail import send_mail
from django.conf import settings
from background_task import background
from templated_email import send_templated_mail

from the_impossible.utils import *

@background(schedule=10)
def welcome_email(username,email,verification_code):
    subject = 'Joined The Impossible'
    message = f"""
        Hi @{username}, thanks for joining The Impossible.
        Your verification code is {verification_code}.
        If you have any questions, please contact hello@theimpossible.world or write us a message from our website.
        You will recieved a weekly update about the latest ideas by email. This can be changed in your newsletter settings.

        Regards
        The Impossible @ 2020
    """
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email,]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except: pass

@background(schedule=10)
def verification_email(email,verification_code):
    send_templated_mail(
        template_name='verification',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        context={
            "date":Date(),
            "verification_code":verification_code
        },
    )

# Check if all notifications are private
def all_private_notification(qs):
    all_private = True
    for notification in qs:
        if notification.message_status != 1:
            all_private = False
            break
    return all_private