from django.db import models

# Create your models here.
from hotel.models import Hotel
from django.core.exceptions import ValidationError
# Create your models here.

def valid_phonenumber(value):
    if value.isdigit():
        if len(value) == 10:
            return value
        else:
            raise ValidationError("Enter 10 digit Number")
    else:
        raise ValidationError("Enter Only Number")

class Contact(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True,blank=True)

    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    phone = models.CharField(max_length=12,validators=[valid_phonenumber])    


    def __str__(self):
        return self.name

    class Meta:
        #verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'