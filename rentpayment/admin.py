from django.contrib import admin

from rentpayment.models import RentPayment

# Register your models here.
class RentPaymentAdmin(admin.ModelAdmin):
    list_display=("id","user","razorpay_payment_id","hotel",'bill_amount',"payment_status","payment_time")
    readonly_fields=("payment_status","razorpay_order_id","razorpay_payment_id","razorpay_signature")

admin.site.register(RentPayment,RentPaymentAdmin)