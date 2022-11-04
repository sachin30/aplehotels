from django.contrib import admin

# Register your models here.
from hotelenquiry.models import HotelEnquiry
from django.utils.html import format_html

# Register your models here.
class HotelEnquiryAdmin(admin.ModelAdmin):
    list_display=("name","email","phone",'subject','message',"hotel")
    list_filter=("hotel",)
    
    list_per_page=10

admin.site.register(HotelEnquiry,HotelEnquiryAdmin)