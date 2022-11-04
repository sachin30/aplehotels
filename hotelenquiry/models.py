from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
from hotel.models import Hotel

def valid_phonenumber(value):
    if value.isdigit():
        if len(value) == 10:
            return value
        else:
            raise ValidationError("Enter 10 digit Number")
    else:
        raise ValidationError("Enter Only Number")

class HotelEnquiry(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=12,validators=[valid_phonenumber])
    message=models.TextField()
    subject=models.CharField(max_length=100)

    class Meta:
        verbose_name = 'HotelEnquiry'
        verbose_name_plural = 'HotelEnquiries'