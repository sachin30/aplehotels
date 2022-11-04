from django.contrib import admin

# Register your models here.
from room.models import Room
from django.contrib.auth.models import User

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display=('hotel','room_type','rent','room_photo','total_room_count')
    list_filter=('room_type','hotel')
    list_per_page=10
    
admin.site.register(Room,RoomAdmin)