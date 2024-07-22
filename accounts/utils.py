

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_email_verification(request, user, mail_subject, mail_template):
    # Email configuration
    sender_email = "wungbrandon27@gmail.com"  # Replace with your Gmail email address
    # sender_email = 'foodonlinepeople23@gmail.com'
    sender_password = 'tgql chcj rwci fcgy' # Replace with your Gmail password
    receiver_email = user.email

    current_site = get_current_site(request)

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = mail_subject

    message = render_to_string(mail_template, {
                 'user': user,
                 'domain': current_site,
                 # encoding the user's uid primary key and send to the email template
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 # takes a user and create a default token
                 'token': default_token_generator.make_token(user)
             })
    # Attach the message to the email
    msg.attach(MIMEText(message, "plain"))


    # Connect to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    # Login to the SMTP server
    server.login(sender_email, sender_password)


    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Disconnect from the server
    server.quit()

    # Success message
    messages.success(request, "Verification email has been sent. Please check your email.")


    return

def send_notification(mail_subject, mail_template, context):
    # sender_email = settings.EMAIL_HOST_USER
    # sender_email = "wungbrandon27@gmail.com"  # Replace with your Gmail email address
    # sender_password = "tgql chcj rwci fcgy"  # Replace with your Gmail password

    sender_email = 'wungbrandon27@gmail.com'
    sender_password = 'tgql chcj rwci fcgy'



    message = render_to_string(mail_template, context)
    to_email = context['to_email']
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = mail_subject

    msg.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()
    return

#
# def send_success(mail_subject, mail_template, context):
#     sender_email = 'wungbrandon27@gmail.com'
#     sender_password = "tgql chcj rwci fcgy"
#
#     message = render_to_string(mail_template, context)
#     to_email = context['user'].email
#     msg = MIMEMultipart()
#     msg["From"] = sender_email
#     msg["To"] = to_email
#     msg["Subject"] = mail_subject
#
#     msg.attach(MIMEText(message, "plain"))
#
#     # Connect to the SMTP server
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, to_email, msg.as_string())
#     server.quit()
#     return
#
