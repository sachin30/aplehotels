
from django.db import models

from room.models import Room
from django.contrib.auth.models import User
# Create your models here.
PAYING_STATUS=(
    ('pending','pending'),
    ('successful','successful'),
    ('failed','failed')
)
class Reservation(models.Model):

    room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='reservations')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    payment_status=models.CharField(choices=PAYING_STATUS,max_length=50,null=True,default="pending")
    created_at=models.DateTimeField()
    total_amount=models.IntegerField()
    rooms_reserved=models.IntegerField()
    def __str__(self):
        return f"{self.room.hotel.name}-{self.room.room_type}-{self.user.first_name}-{self.payment_status}-{self.rooms_reserved}-{self.start_date} to {self.end_date}"

    @property
    def room_name(self):
        return f"{self.room}"