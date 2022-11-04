from django.contrib import admin

from review.models import Review
from django.contrib.auth.models import User
from django.utils.html import format_html


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display=('user','hotel','review','user_rating')
    list_per_page=10
    

    def user_rating(self,obj):
        return format_html(f"<span style='color:red'><b>{obj.rating}</b></span>")
admin.site.register(Review,ReviewAdmin)