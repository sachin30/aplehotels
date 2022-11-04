import csv
from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from hotel.models import Amenity, Hotel
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib import messages
from import_export.admin import ExportActionMixin
from import_export.admin import ImportMixin
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class HotelAdmin(ImportExportModelAdmin,ExportActionMixin):
   
    
    prepopulated_fields = {
        'slug': ['name','city'],
    }
    # fields=("title","address","city","state","zipcode","photo_main","description","slug","bedrooms","bathrooms","sqft","plot_size","slug")
    readonly_fields=("photo_preview",)
    list_display= ("name",'id','hotelmanager',"address","city","state",'get_amenities',"photo_preview","less_description","rating","customer_visits","rating_customers","view","slug")
    list_filter=('city',)
    #list_display_links=("title","less_description")
    # radio_fields={"bedrooms":admin.HORIZONTAL}  #if you hide/remove this radio field option then it will show default select box
    save_on_top= True
    ordering = ('-id',)
    search_fields=("name","address","city","state")
    list_per_page=10

    #Actions------------------------------------------------------------------------------------------------
    #actions = ['export_pdf']        #no quotes if action method is outside of class

    def less_description(self,obj):
        return format_html(f"<span id='new'>{obj.description[:50]}</span>")

    def view(self,obj):
        return format_html(f"<button id='view button'  class='button'>View</button>")

    def photo_preview(self,obj):
        return format_html(f"<img src='/media/{obj.main_photo}' style='height:100px ;width:100px' >")

    def rating(self,obj):
        return format_html(f"<span style='color:red'>{round(obj.get_average_rating(),1)}</span>")

    # @admin.action(description='Export selected as CSV')
    # def export_pdf(self, request, queryset):      #modeladmin instead of self if this method is outside of This class
    #     response=HttpResponse(content_type="text/csv")
    #     response["Content-Disposition"]="attachment; filename=excel.csv"
    #     print(vars(response))
    #     #create csv writer
    #     writer=csv.writer(response)
        
    #     # properties=Property.objects.all()

    #     #1st row in csv
    #     writer.writerow(["Name","Address","Description","State","City","Zipcode","Photo","Slugurl","Rating","Rating_Customers","Amenities"])
    #     #remaining rows
    #     for hotel in queryset:
    #         writer.writerow([hotel.name,hotel.address,hotel.description,hotel.state,hotel.city,hotel.zipcode,hotel.main_photo,hotel.slug,hotel.total_rating,hotel.rating_customers,[amenity.id for amenity in hotel.amenity.all()]])
    #     # self.message_user(request, ngettext(
    #     #         '%d hotel was successfully added to csv.',
    #     #         '%d hotels were successfully added to csv.',
    #     #         queryset,
    #     #     ) % len(queryset), messages.SUCCESS)
    #     return response

    # def readonly_slug(self,obj):
    #     return format_html(f"<span style='color:red'>{obj.slug}</span>")

admin.site.register(Hotel,HotelAdmin)
admin.site.register(Amenity)
# admin.site.add_action(export_pdf)
