from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(token):
    send_mail(
        subject="Please Cofirm your email",
        message=f"Use this link to confirm your email: http://127.0.0.1:8000/confirm/{token.token}/",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[token.user.email]
    )



def send_reset_password_email(token):
    send_mail(
        subject="Reset your password",
        message=f"Use this link to reset your password: http://127.0.0.1:8000/reset-password/{token.token}/",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[token.user.email]
    )

