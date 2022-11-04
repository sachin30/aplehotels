from django.contrib import admin

# Register your models here.
from django import forms
from hotelmanager.models import HotelManager
from django.utils.html import format_html


# # class HotelManagerForm(forms.ModelForm):
#     class Meta:
#         widgets = {                         
#             'phone': PhoneNumberPrefixWidget(initial='IN'),
#         }
# # Register your models here
class HotelManagerAdmin(admin.ModelAdmin):
    
    def manager_photo(self,obj):
        return format_html(f"<img src='/media/{obj.photo}' style='height:100px ;width:100px' >")

    list_display=("first_name","last_name",'email',"address","manager_phone","manager_photo")
    list_per_page=10


admin.site.register(HotelManager,HotelManagerAdmin)

