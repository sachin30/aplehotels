from time import sleep
import time
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from hotel.models import Hotel

@shared_task(bind=True)
def enquiry_hotel_mail(self,subject,user_email,message,hotel_id):
    hotel=Hotel.objects.get(pk=hotel_id)
    manager_email=hotel.hotelmanager.email
    print(manager_email)
    #email_to='sachin.esenceweb@gmail.com'
    #send mail to admin
    send_mail(subject,message,settings.EMAIL_HOST_USER,[manager_email],fail_silently=False)

    message2="Dear Customer\n\t Thank you for Contacting us, Your queries will be solved shortly.\n Our support will reach u as soon as possible."
    #send thank you mail to user
    send_mail(f"From {hotel.name}",message2,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
    
    return "Email sent Successfully"