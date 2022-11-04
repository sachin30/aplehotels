from time import sleep
import time
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def contact_us_mail(self,subject,user_email,message):
    email_to='sachin.esenceweb@gmail.com'
    #send mail to admin
    send_mail(subject,message,settings.EMAIL_HOST_USER,[email_to],fail_silently=False)

    message2="Dear Customer\n\t Thank you for Contacting us, Your queries will be solved shortly.\n Our support will reach u as soon as possible."
    #send thank you mail to user
    send_mail('From Hotels',message2,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
    
    return "Email sent Successfully"

@shared_task(bind=True)
def send_mail_everyday(self):
    send_mail('subject','message',settings.EMAIL_HOST_USER,['sachinpandhare1996@gmail.com'])
    return 'daily email sent'