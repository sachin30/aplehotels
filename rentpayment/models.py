from django.db import models
from django.contrib.auth.models import User
from hotel.models import Hotel
from room.models import Room

# Create your models here.
class RentPayment(models.Model):
    STATUS=(
        ("pending","pending"),
        ("success","success"),
        ("failure","failure"),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,null=True,blank=True)
    payment_time=models.DateTimeField(blank=True,null=True)
    bill_amount=models.CharField(max_length=10,blank=True,null=True)
    
    payment_status=models.CharField(choices=STATUS,default="pending",max_length=10,blank=False,null=False)
    
    razorpay_payment_id=models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id=models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature=models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.id}-{self.user}-{self.hotel}-{self.payment_status}"

    

    # @property
    # def booking_status(self):
    #     return self.room.booking_status

    # @booking_status.setter
    # def booking_status(self,value):
    #     self.room.booking_status=value

