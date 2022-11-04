from django.contrib import admin

# Register your models here.
from contact.models import Contact

# Register your models here.
class ContactsAdmin(admin.ModelAdmin):
    list_display=('name',"email","subject","message","phone")
    list_per_page=10

admin.site.register(Contact,ContactsAdmin)