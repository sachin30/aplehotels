from django.urls import path
from django.contrib.auth import views as auth_views
from pages import views
app_name="pages"
urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('about_us/',views.about_us,name="about_us"),   
    path('userlogout',views.userlogout,name="userlogout"),
    path("display_hotels",views.display_hotels,name="display_hotels"),
    path("display_rooms/<str:hotel_id>",views.display_rooms,name="display_rooms"),
    path("booking_details_and_book",views.booking_details_and_book,name="booking_details_and_book"),
    path("room_book/<str:hotel_id>",views.room_book,name="room_book"),
    path("contact/",views.contact, name="contact"),
    path("userlogin/",views.userlogin,name="userlogin"),
    path("registration/",views.registration,name="registration"),
    path("save_review/",views.save_review, name="save_review"),
    path("hotel_enquiry/",views.hotel_enquiry, name='hotel_enquiry'),
    path("payment_page/<str:hotel_id>",views.payment_page,name="payment_page"),
    path("handlerequest/",views.handlerequest,name='handlerequest'),
    path("my_profile/",views.my_profile,name="my_profile"),
    path("user_reservations/",views.user_reservations,name="user_reservations"),
    path("import_csv/",views.import_csv,name='import_csv'),
    #ajax paths for hotel updating
    path("hotel_ajax_save/",views.hotel_ajax_save,name='hotel_ajax_save'),

    path("change_password/",views.change_password,name='change_password'),
    # path("user_details/",views.user_details,name="user_details"),
]
