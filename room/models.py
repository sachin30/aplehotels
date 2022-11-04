

from django.db import models
# from django.contrib.auth.models import User
from hotel.models import Hotel

ROOM_TYPE=(
    ('standard','standard'),
    ('suite','suite'),
    ('deluxe','deluxe')
)

# PAYMENT_STATUS=(
#     ('pending','pending'),
#     ('failed','failed'),
#     ('successful','successful')
# )
BOOKING_STATUS=(
    ('available','available'),
    ('booked','booked')
)
# Create your models here.
class Room(models.Model):       
   
    total_room_count=models.IntegerField()
    # user=models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='rooms')
    room_type=models.CharField(max_length=50,choices=ROOM_TYPE)
    # size=models.IntegerField()
    rent=models.IntegerField()
    # checkin=models.DateTimeField(blank=True,null=True)
    # checkout=models.DateTimeField(blank=True,null=True)
    room_photo=models.ImageField(upload_to="room")
    # room1=models.ImageField(upload_to="room",blank=True)
    # room2=models.ImageField(upload_to="room",blank=True)
    # room3=models.ImageField(upload_to="room",blank=True)
    # booking_status=models.CharField(max_length=50,choices=BOOKING_STATUS,blank=True,null=True)
    #payment_status=models.CharField(max_length=50,choices=PAYMENT_STATUS,blank=True,null=True)
    # total_bill=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.hotel}-{self.room_type}"

    def get_absolute_url(self):
        return "/payment_page/%i" % self.hotel.id


    @property
    def room_city_filter_field(self):
        return self.hotel.city
    

    