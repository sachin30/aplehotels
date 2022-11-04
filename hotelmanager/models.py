from django.db import models

# Create your models here.
import numbers
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

def valid_phonenumber(value):
    if value.isdigit():
        if len(value) == 10:
            return value
        else:
            raise ValidationError("Enter 10 digit Number")
    else:
        raise ValidationError("Enter Only Number")

# Create your models here.
class HotelManager(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    manager_phone = models.CharField(max_length=12,validators=[valid_phonenumber])   
    photo=models.ImageField(upload_to="hotel_owner")
    address=models.CharField(max_length=100)
    email=models.EmailField()
    
    def __str__(self):
        return self.first_name

