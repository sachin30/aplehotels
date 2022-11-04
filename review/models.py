
from django.db import models
from django.contrib.auth.models import User
from hotel.models import Hotel

RATING_STARS=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)
# Create your models here.
class Review(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,blank=True,null=True)
    review=models.TextField()
    rating=models.CharField(choices=RATING_STARS,null=True,default='2',max_length=10)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    
