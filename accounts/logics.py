from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

FROM_EMAIL = settings.EMAIL_HOST_USER


def send_email(user, email_type="") -> bool:
    subject = ""
    plain_content = ""

    if email_type == "otp_verification":
        subject = "OTP for email verification."
        html_content = render_to_string(
            "./templates/email.html",
            {"username": user.username, "otp": user.otp, "subject": subject},
        )
        plain_content = strip_tags(html_content)

    if email_type == "otp_verified":
        subject = "Your email is verified."
        html_content = render_to_string(
            "./templates/email.html",
            {
                "username": None,
                "message": "Your email is verified, now you can login to your app.",
                "subject": subject,
            },
        )
        plain_content = strip_tags(html_content)

    if not subject or not plain_content or not FROM_EMAIL:
        return False

    # Create EmailMultiAlternatives instance
    msg = EmailMultiAlternatives(subject, plain_content, FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True
