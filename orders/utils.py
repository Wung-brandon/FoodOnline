from datetime import datetime
from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages


def generate_order_number(pk):
    current_datetime = datetime.now().strftime('%Y%m%d') # 202312031320 + pk
    order_number = current_datetime + str(pk)
    return order_number

def orders_completed():
    pass
