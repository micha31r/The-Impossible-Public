from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False