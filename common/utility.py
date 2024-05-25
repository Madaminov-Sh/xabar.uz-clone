import random

from django.core.mail import send_mail

from config.settings import EMAIL_HOST, EMAIL_HOST_USER

def generate_code():
    code = "".join([str(random.randint(0, 10000) % 10) for _ in range(5)])
    return code


def send_email(code, email):
    subject = "Verification code"
    message = "Your verification code is: ", code
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[email])