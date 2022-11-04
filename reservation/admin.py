from django.contrib import admin

from reservation.models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display=('room','user','payment_status','start_date','end_date','rooms_reserved')
    search_fields=('payment_status','room')
    list_filter=('payment_status','room')
# Register your models here.
admin.site.register(Reservation,ReservationAdmin)