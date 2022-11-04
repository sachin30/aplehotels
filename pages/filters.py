import django_filters
from django import forms
from django_filters import CharFilter
from hotel.models import AMENITIES, Hotel, Amenity
from room.models import Room


class HotelFilter(django_filters.FilterSet):
    city=CharFilter(field_name="city",lookup_expr="icontains")
    available_rooms=django_filters.NumberFilter(field_name="available_rooms",lookup_expr="gte")

    # amenity=Amenity.objects.all()
    
    # amenities = django_filters.ModelMultipleChoiceFilter(
    #         queryset=amenity,
    #         label="Amenities",
    #     )

    class Meta:
        model=Hotel
        fields=('city',)


class RoomFilter(django_filters.FilterSet):
    CHOICES=(
        ('low to high',"Rent- Low to High"),
        ('high to low',"Rent- High to Low")
    )
    rent = django_filters.NumberFilter(field_name="rent",lookup_expr='lt')
    ordering =django_filters.ChoiceFilter(label="ordering", choices=CHOICES, method='filter_by_order')
    class Meta:
        model=Room
        fields=('room_type','rent')

    def filter_by_order(self,queryset,name,value):
        rent='rent' if value=='low to high' else '-rent'
        return queryset.order_by(rent)



