
from django.db import models

# Create your models here.
from hotelmanager.models import HotelManager
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError


AMENITIES=(
    ('big bed','big bed'),
    ('hot water','hot water'),
    ('wifi','wifi'),
    ('free breakfast','free breakfast'),
    ('coffee','coffee'),
    ('television','television'),
    ('sanitization','sanitization'),
    ('medic kit','medic kit'),
)

# Create your models here.
class Amenity(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name='Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name

class Hotel(models.Model):
    
    hotelmanager=models.OneToOneField(HotelManager, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    description=models.TextField()
    amenity = models.ManyToManyField(Amenity)               #Many to many field for amenities

    #amenities = MultiSelectField(max_length=200,choices=AMENITIES)
    
    # bathrooms=models.CharField(max_length=2,choices=BEDROOM_CHOICES,blank=True,null=True)
    main_photo=models.ImageField(upload_to='uploads/%Y/%m/%d/')
    photo_2=models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    photo_3=models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    photo_4=models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    zipcode=models.IntegerField(blank=True)
    #total_rooms=models.IntegerField(blank=True,null=True)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    #available_rooms=models.IntegerField(blank=True,null=True)
    total_rating=models.FloatField(blank=True,null=True)
    customer_visits=models.IntegerField(blank=True,null=True)
    rating_customers=models.IntegerField(blank=True,null=True)
    slug=models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

    def __str__(self):
        return self.name.capitalize()

    def get_average_rating(self):
        return self.total_rating/self.rating_customers

    @property
    def get_all_available_rooms(self):
        return self.room_set.filter(booking_status='available')

    def get_absolute_url(self):
        return "/display_rooms/%i" % self.id

    @property
    def get_amenities(self):
        new_list=[]
        for i in self.amenity.all():
            new_list.append(str(i))
        return new_list 
