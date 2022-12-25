
from django.shortcuts import render
from django.http import HttpResponse,BadHeaderError,HttpResponseRedirect,JsonResponse
from hotelenquiry.models import HotelEnquiry
from hotels.forms import HotelEnquiryForm, RegistrationForm,ContactForm, ReviewForm
from django.contrib import messages
from pages.decorators import *
from django.contrib.auth import login,authenticate,logout
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from hotel.models import Amenity, Hotel
from rentpayment.models import RentPayment
from reservation.models import Reservation
from room.models import Room
from review.models import Review
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
import razorpay
from django.db.models import F,Q,Count,Sum,Case,When
from pages.filters import HotelFilter, RoomFilter
from datetime import timedelta
import pandas
from django.core.files.storage import FileSystemStorage
#Celery
#this is for admin field to update data on mouse double click js event
@loginfirst
def hotel_ajax_save(request):
    if request.method == "POST":    
        hotel_id=request.POST["hotel_id"]
        field = request.POST["field_name"]
        data = request.POST['data']
        print(hotel_id,field,data)
        if hotel_id.isdigit():
            hotel=Hotel.objects.get(pk=hotel_id)
            if field == 'field-city':   
                print("field is city") 
                hotel.city=data
                hotel.save()

            if field == 'field-address':   
                print("field is address") 
                hotel.address = data
                hotel.save()

            if field == 'field-state':   
                print("field is state") 
                hotel.state = data
                hotel.save()
        else:
            return JsonResponse({"status":"in admin page change_list, id column should be 2nd"})

        return JsonResponse({"status":"successful"})
    else:
        return HttpResponse('you are not supposed to directly jump to this page')


# Create your views here.
def import_csv(request):
    print("in import csv")
    print(vars(request.FILES))
    if request.method=="POST" and request.FILES["myfilename"]:
        myfile=request.FILES["myfilename"]
        
        #save to file storage
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        file_upload_url=fs.url(filename)
        excelfile=file_upload_url
        property_excel_data=pandas.read_csv('.'+excelfile, encoding="utf-8")
        dbframe=property_excel_data
        rows = len(dbframe.axes[0])
        cols = len(dbframe.axes[1])
        
       
        for dbframe in dbframe.itertuples():
            obj=Hotel.objects.create(name=dbframe.Name,
                                        address=dbframe.Address,
                                        description=dbframe.Description,
                                        state=dbframe.State,    
                                        city=dbframe.City,
                                        
                                        zipcode=dbframe.Zipcode,
                                        main_photo=dbframe.Photo,
                                        slug=dbframe.Slugurl,
                                        total_rating=dbframe.Rating,
                                        rating_customers=dbframe.Rating_Customers
                                        
                                        )
            if dbframe.Amenities != '':
                amenities=dbframe.Amenities[1:-1]
                amenity_list=amenities.split(',')
                print(amenity_list)
                print(type(amenity_list))
                
                obj.amenity.add(*amenity_list)
            obj.save()
        messages.success(request,f"{rows} {'Hotel was' if rows == 1 else 'Hotels were'} added using Import csv Functionality")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return JsonResponse({"status":"failed"})


@loginfirst
def my_profile(request):
    return render(request,'pages/my_profile.html')

@loginfirst
def change_password(request):
    if request.method == 'POST':
        print('change password')
        p1=request.POST['change_password1']
        p2=request.POST['change_password2']
        if p1 == p2:
            u=User.objects.get(username=request.user.username)
            u.set_password(p1)
            u.save()
            return JsonResponse({"status":"success"})
        else:
            return JsonResponse({"status":"failed"})
    else:
        return HttpResponseRedirect('/my_profile')

@loginfirst
def user_reservations(request):
    if request.method == "POST":    
        print("getting reservations")

        old_reservations=Reservation.objects.filter(user__username=request.user.username).filter(end_date__lt=datetime.now()).values('id','start_date','end_date','payment_status','total_amount','rooms_reserved',room_type=F('room__room_type'),hotel=F('room__hotel__name'))
        print("values",old_reservations)
        old_reservations=list(old_reservations)

        active_reservations=Reservation.objects.filter(user__username=request.user.username).filter(end_date__gte=datetime.now()).values('id','start_date','end_date','payment_status','total_amount','rooms_reserved',room_type=F('room__room_type'),hotel=F('room__hotel__name'))
        print("values",active_reservations)
        active_reservations=list(active_reservations)
        
            
        return JsonResponse({"status":"success","old_reservations":old_reservations,"active_reservations":active_reservations})
    else:
        return JsonResponse({'status':"failed"})
def homepage(request):
    #print(dir(request))
    #print(request.COOKIES)
    hotel_list=Hotel.objects.all()
    hotel_filter=HotelFilter(queryset=hotel_list)
    context={'hotel_filter':hotel_filter}
    return render(request,'pages/homepage.html',context)

def about_us(request):
    return render(request,'pages/about_us.html')

@unauthenticateduser
def registration(request):
    form=RegistrationForm()
    
    context={}
    if request.method=="POST":
    
        #create form object
        form=RegistrationForm(request.POST) 
        print(vars(form))
        for field in form:
            print("Field Error:", field.name,  field.errors)
        print(form.is_valid())
        if form.is_valid(): 
            print("form is valid")
            form.save()
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get('password1')
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,"Customer registered successful: "+username)
                messages.success(request,'You Are Logged in as - '+ username)
                return HttpResponseRedirect('/')
                
        else:
            form_err=form.errors
            context={"form_err":form_err,"form":form}
            return render(request,"pages/registration.html",context)
    
    
    context['form']= form
    
    return render(request,"pages/registration.html",context)

@unauthenticateduser
def userlogin(request):
    print(vars(request.session))
    if request.method == 'POST':
        name=request.POST['Name']
        password=request.POST['Password']
        
        user=authenticate(request,username=name,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'You Are Logged in as - '+ name)
            print(vars(request.session))
            if "user_booking" in request.session:
                room_id=request.session['room_id']
                room_obj=Room.objects.get(pk=room_id)
                return redirect(room_obj)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Wrong Credentials")
            return HttpResponseRedirect('/userlogin')


    return render(request,'pages/login.html')

@loginfirst
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/userlogin')


def contact(request):
  
    form=ContactForm()
    context={}
    if request.method=="POST":
       
        #create form object
        form=ContactForm(request.POST) 
        
        for field in form:
            print("Field Error:", field.name,  field.errors)
        print(form.is_valid())
        if form.is_valid():
            print("form is valid")
            form.save()
            
            
            #sending mail to manager
            # name=form.cleaned_data["name"]
            # email=form.cleaned_data["email"]
            # subject=form.cleaned_data["subject"]
            # message=form.cleaned_data["message"]
            # phone=form.cleaned_data["phone"]
            # message="\t"+name+" is trying to contact us for some information and left a message:\n\t"+message+"\n\nEmail : "+email+"\nPhone Number : "+phone
           
            # #Use Gmail's app password by turning 2step verification ON.
            # #Then generate new app password.use that pass as USER_HOST_PASSWORD        
            # email_from=settings.EMAIL_HOST_USER
            # email_to="sachin.esenceweb@gmail.com"
        
            #create email object
            #email_message= EmailMessage(subject, message, email_from, [email_to])

            #email to customer
            #message2="Dear Customer\n\t Thank you for Contacting us, Your queries will be solved shortly.\n Our support will reach u as soon as possible."
            # thank_email=EmailMessage('From Hotels',message2,email_from,[email])
        
 
            try:
                #send from the function within forms.py(contact) 
                form.send_email()
                #send email
                # email_message.send(fail_silently=False)
                # thank_email.send(fail_silently=False)
                messages.success(request,"Thanks for your Interest, We will contact you soon")

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponseRedirect('/')
        else:
            print("form is invalid")
            form_err=form.errors
            context={"form_err":form_err,"form":form}
            return render(request,"pages/contact.html",context)
        
    context['form']= form
    return render(request,"pages/contact.html",context)


def display_hotels(request):
    
    context={}
    if request.method=="POST":
        city=request.POST.get('city')
        book_from=request.POST.get('book_from')
        book_till=request.POST.get('book_till')
        room_count=request.POST.get('room_count')
        room_type=request.POST.get('room_type')
        print(city,book_from,book_till,room_count,room_type)
        request.session.get('city', city)
        request.session['city']=city
        request.session.get('book_from','')
        request.session['book_from']=book_from
        request.session.get('book_till', book_till)
        request.session['book_till']=book_till
        request.session.get('room_count', room_count)
        request.session['room_count']=room_count
        request.session.get('room_type', room_type)
        request.session['room_type']=room_type

        print(vars(request.session))
        hotels=Hotel.objects.filter(rooms__room_type=room_type).filter(city__icontains=city)
        print('hotels                        ',hotels)
       
        #reservations=Reservation.objects.filter(start_date__gte=book_from,end_date__lte=book_till) & Reservation.objects.filter(payment_status='successful') & Reservation.objects.filter(room__room_type=room_type)  
        #reservations=reservations.annotate(Sum('rooms_reserved'))
        #total_successful_reserved_rooms=Sum('')

        # rooms1=Room.objects.filter(room_type=room_type).annotate(total_reserved_rooms=Sum('reservations__rooms_reserved')).annotate(available_rooms=F('total_room_count')-F('total_reserved_rooms')).filter(available_rooms__lte=room_count).filter(total_room_count__lte=F('total_reserved_rooms'))
        
        # print('room1 count exclusion rooms  ',rooms1)

        #rooms1=Room.objects.filter(room_type='standard').annotate(total_reserved_rooms=Case(When(reservations__payment_status='successful'),then=Value(Sum('reservations__rooms_reserved')))).annotate(available_rooms=F('total_room_count')-F('total_reserved_rooms')).filter(available_rooms__lte=4).filter(total_room_count__lte=F('total_reserved_rooms'))

        #rooms1=Room.objects.filter(room_type=room_type).annotate(total_reserved_rooms=Sum(Case(When(reservations__payment_status='successful',then=F('reservations__rooms_reserved')),default=0))).annotate(available_rooms=F('total_room_count')-F('total_reserved_rooms')).filter(available_rooms__lte=room_count)#.filter(total_room_count__lte=F('total_reserved_rooms'))

        rooms=Room.objects.filter(room_type=room_type).annotate(total_reserved_rooms=Sum(Case(When(Q(reservations__payment_status='successful') & Q(reservations__start_date__gte=book_from) & Q(reservations__end_date__lte=book_till),then=F('reservations__rooms_reserved')),default=0))).annotate(available_rooms=F('total_room_count')-F('total_reserved_rooms')).filter(available_rooms__lt=room_count)

        for room in rooms:
            print(room,'               ',vars(room))
        # reservations_list=Reservation.objects.filter(Q(start_date__gte=book_from) & Q(end_date__lte=book_till) & Q(payment_status='successful') & Q(room__room_type=room_type)) 
        # print('reservations list            ',reservations_list)
        # reservation_id_list=[]
        # for reservation in reservations_list:
        #     reservation_id_list.append(int(reservation.id))
        # print(reservation_id_list)
        # rooms2=rooms1.filter(reservations__in=reservations_list)
        # print('reserved rooms2               ',rooms2)

        #rooms=rooms1.filter(Q(reservations__start_date__gte=book_from) & Q(reservations__end_date__lte=book_till) & Q(reservations__payment_status='successful'))
        
        
        # print('reserved rooms3 for exclusion',rooms3)
        # rooms=rooms1 | rooms3
        print(rooms)
        hotel_list=hotels.exclude(rooms__in=rooms).distinct().annotate(room_rent=F('rooms__rent')).order_by(F('room_rent'))
        
        #paginate
        paginator = Paginator(hotel_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        print("rooms with reserved count")
        print(rooms)
        # context['hotels']=hotel_list
        context={'hotels':page_obj,'city':city,'book_from':book_from,'book_till':book_till,'room_count':room_count,'room_type':room_type}
        # for room in rooms:
        #     #room.refresh_from_db()
        #     print(vars(room))
        #     print(room,room.total_reserved_rooms)
        #rooms=rooms.filter(total_room_count__gt=F('total_reserved_rooms'))
        
        # print("with greater than condition")
        # for room in rooms:
        #     #room.refresh_from_db()
        #     print(vars(room))
        #     print(room,room.total_reserved_rooms)
        
        # for reservation in reservations:
        #     print(vars(reservation))

        # if room_type=='suite':
        #     hotels=Hotel.objects.filter(rooms__room_type='suite').filter(city__icontains=city)
        #     print(hotels)
            
        #     reservations=Reservation.objects.filter(start_date__gte=book_from,end_date__lte=book_till) & Reservation.objects.filter(payment_status='successful') & Reservation.objects.filter(room__room_type='suite')  
        #     #reservations=reservations.annotate(Sum('rooms_reserved'))
        #     rooms=Room.objects.annotate(total_reserved_rooms=Sum('reservation__rooms_reserved')) & Room.objects.filter(room_type='suite')

        #     hotel_list=hotels.exclude(room__in=rooms).distinct
        #     print(hotel_list)
        #     for room in rooms:
        #         print(vars(room))
        #         print(room,room.total_reserved_rooms)
            

        #     # for reservation in reservations:
        #     #     print(vars(reservation))
        
        # if room_type=='deluxe':
        #     pass
    # if request.method == "POST":
    #     amenities=Amenity.objects.all()
    #     hotels=Hotel.objects.all().order_by('-id')
        
    #     if "amenity_form_button" in request.POST:
    #         amenity_list=request.POST.getlist('amenity')
    #         print(amenity_list)
    #         amenitys=[]
    #         for ame in amenity_list:
    #             amenitys.append(int(ame))
    #         print(amenitys)
    #         if amenitys:

    #             hotels=hotels.filter(Q(amenity__in = amenitys)).distinct()
                
    #             print(hotels)
    #             hotels=hotels.annotate(Count('amenity')).order_by('-amenity__count')
    #             for hotel in hotels:
    #                 print(hotel.amenity__count)
               
                
    #         print(hotels)
    #         context={"hotels":hotels,"amenities":amenities}

    #         return render(request,"pages/display_hotels.html",context)
      
            

    #     print("in post")
        
    #     print(vars(request.POST))
    #     hotels=Hotel.objects.all()
    #     hotel_list=HotelFilter(request.POST,queryset=hotels)
    #     print(hotel_list.filters)
    #     print(vars(hotel_list.filters))
    #     hotels=hotel_list.qs

    #     context={"hotels":hotels,"amenities":amenities}

    #     return render(request,'pages/display_hotels.html',context)
        

    # amenities=Amenity.objects.all()
    # hotels=Hotel.objects.all().order_by('-id')
    # paginator = Paginator(hotels, 10) 

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # context={'hotels':page_obj,'amenities':amenities}
        
    return render(request,'pages/display_hotels.html',context)

def display_rooms(request,hotel_id):

   
    hotel=Hotel.objects.get(pk=hotel_id)
    
    rooms=hotel.rooms.all()

    reviews=Review.objects.filter(hotel=hotel).order_by('-id')

    form = ReviewForm()
    enquiry_form=HotelEnquiryForm()
    if 'room_type' in request.session:
        print('data is present')

    #total_days=request.session['data']['book_till'] - request.session['data']['book_from']
    book_till_date=datetime.strptime(request.session['book_till'],"%Y-%m-%d").date()
    book_from_date=datetime.strptime(request.session['book_from'],"%Y-%m-%d").date()
    print(book_from_date)
    print(str(book_till_date))
    date_info=book_till_date-book_from_date
    total_days=pandas.Timedelta(date_info)
    room=hotel.rooms.filter(room_type=request.session['room_type'])
    #set session variables
    request.session.get('room_id', room[0].id)
    request.session['room_id']=room[0].id
    request.session.get('room_rent', room[0].rent)
    request.session['room_rent']=room[0].rent
    request.session.get('total_days', total_days.days)
    request.session['total_days']=total_days.days
    total_bill=int(request.session['room_count']) * int(request.session['room_rent']) * int(request.session['total_days'])
    
    # print('date_info',date_info)
    # # print('days in int',type(date_info.days))
    # request.session.get('book_from_date', book_from_date)
    # request.session['book_from_date']=book_from_date
    # request.session.get('book_till_date', book_till_date)
    # request.session['book_till_date']=book_till_date
    
    request.session.get('total_bill', total_bill)
    request.session['total_bill']=total_bill
    

    # request.session['data']['book_from_date']=book_from
    # request.session['data']['book_till_date']=book_till
    # request.session['data']['total_days']=date_info.days
    # room=hotel.rooms.filter(room_type=request.session['data']['room_type'])
    # request.session['data']['room_rent']=room[0].rent
    # request.session['data']['total_bill']=int(request.session['data']['room_count']) * int(request.session['data']['room_rent']) * int(request.session['data']['total_days'])
    
    #request.session['data']['total_bill']=
    print((total_days))
    print(vars(request.session))

    # if request.method == "POST":
    #     print("in display rooms post")
    #     hotel=Hotel.objects.get(pk=hotel_id)
    #     #hotel_name=hotel.name
    #     print(request.POST)
    #     rooms=hotel.rooms.all()
    #     filtered_rooms=RoomFilter(request.POST,queryset=rooms) 
    #     rooms=filtered_rooms.qs
    #     # paginator = Paginator(rooms, 10) 
        # if 'btn' in request.POST:
        #     print('explore button clicked')
        #     city=request.POST.get('city')
        #     book_from=request.POST.get('start_date')
        #     book_till=request.POST.get('end_date')
        #     room_count=request.POST.get('room_count')
        #     room_type=request.POST.get('room_type')
        #     print(city,book_from,book_till,room_count,room_type)

        #     return JsonResponse({'status':'successful','city':city,'book_from':book_from,'book_till':book_till,'room_count':room_count,'room_type':room_type})
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        # reviews=Review.objects.filter(hotel=hotel)

        # form = ReviewForm()
        # enquiry_form=HotelEnquiryForm()
            
        # context={'rooms':rooms,'hotel':hotel, 'reviews':reviews,'form':form,'enquiry_form':enquiry_form,'filtered_rooms':filtered_rooms}
        
        # return render(request,'pages/display_rooms.html',context)
    
    context={'rooms':rooms,'hotel':hotel, 'reviews':reviews,'form':form,'enquiry_form':enquiry_form}
    
    return render(request,'pages/display_rooms.html',context)

def booking_details_and_book(request,hotel_id):
    
    hotel=Hotel.objects.filter(pk=hotel_id)
    context={'hotel':hotel}
    return render(request,'pages/booking_details_and_book.html',context)

def room_book(request,hotel_id):
    print('room book')
    context={}
    if request.user.is_authenticated:
        hotel=Hotel.objects.get(pk=hotel_id)
        
        book_till_date=datetime.strptime(request.session['book_till'],"%Y-%m-%d").date()
        book_from_date=datetime.strptime(request.session['book_from'],"%Y-%m-%d").date()
        date_info=book_till_date-book_from_date
        total_days=pandas.Timedelta(date_info)
        room=hotel.rooms.filter(room_type=request.session['room_type'])
        #set session variables
        request.session.get('room_id', room[0].id)
        request.session['room_id']=room[0].id
        request.session.get('room_rent', room[0].rent)
        request.session['room_rent']=room[0].rent
        request.session.get('total_days', total_days.days)
        request.session['total_days']=total_days.days
        total_bill=int(request.session['room_count']) * int(request.session['room_rent']) * int(request.session['total_days'])
        
        
        request.session.get('total_bill', total_bill)
        request.session['total_bill']=total_bill
        #the room model contains 'get_absolute_url' to payment page
        return redirect(room[0])
    else:
        hotel=Hotel.objects.get(pk=hotel_id)
        
        book_till_date=datetime.strptime(request.session['book_till'],"%Y-%m-%d").date()
        book_from_date=datetime.strptime(request.session['book_from'],"%Y-%m-%d").date()
        date_info=book_till_date-book_from_date
        total_days=pandas.Timedelta(date_info)
        room=hotel.rooms.filter(room_type=request.session['room_type'])
        #set session variables
        request.session.get('room_id', room[0].id)
        request.session['room_id']=room[0].id
        request.session.get('room_rent', room[0].rent)
        request.session['room_rent']=room[0].rent
        request.session.get('total_days', total_days.days)
        request.session['total_days']=total_days.days
        total_bill=int(request.session['room_count']) * int(request.session['room_rent']) * int(request.session['total_days'])
        
        
        request.session.get('total_bill', total_bill)
        request.session['total_bill']=total_bill
        user_booking=request.session.get('user_booking',1)      
        request.session['user_booking'] = user_booking          #used in userlogin view
        
        
        
        #print('user booking:',request.session['user_booking'])
        # print('room id',request.session['room_id'])
        
        return HttpResponseRedirect('/userlogin')

#save review using ajax
def save_review(request):
    if request.method == 'POST':
        print("in review post method")
        hotel=request.POST.get('hotel')
        user=request.POST.get('user')
        rating=request.POST.get('rating')
        review_data=request.POST.get('review')
        id=request.POST.get('review_id')
        existing_review_rating=request.POST.get('existing_review_rating')
        user=User.objects.get(pk=user)
        hotel=Hotel.objects.get(pk=hotel)
        #typecast
        if existing_review_rating is not None and existing_review_rating !='':
            existing_review_rating=float(existing_review_rating)

        if rating is not None:
            if rating != '':
                rating=float(rating)

        if id is None:
            print("adding rating and customer")
            hotel.total_rating=F('total_rating') + float(rating)
            #hotel.total_rating += float(rating)
            #hotel.rating_customers += 1
            hotel.rating_customers=F('rating_customers') + 1
            hotel.save()
            review=Review(hotel=hotel,user=user,rating=int(rating),review=review_data)
        else:
            if existing_review_rating is not None and existing_review_rating != '':
                if rating is not None and rating != '':
                    print("new and old rating present")
                    if existing_review_rating > rating:
                        difference = existing_review_rating - rating
                        print("rating decreased")
 
                        print(hotel.total_rating)
                        hotel.total_rating -= float(difference)
                        hotel.save()
                        print(hotel.total_rating)
                        
                    if existing_review_rating < rating:
                        difference=rating - existing_review_rating
                        print("rating increased")

                        print(hotel.total_rating)
                        hotel.total_rating += float(difference)
                        hotel.save()
                        print(hotel.total_rating)
                else:
                    print("new rating is zero")
                    hotel.total_rating -= existing_review_rating
                    hotel.save()
                    print(hotel.total_rating)
            else:
                print("old rating is null")
                if rating is not None and rating != '':
                    print("new rating is present")
                    hotel.total_rating += rating
                    hotel.save()
                    print(hotel.total_rating)
                else:
                    print("both values are zero so no change")
            review=Review(id=id,hotel=hotel,user=user,rating=int(rating),review=review_data)
            
        object_info=vars(review)
        user_id=object_info.get('user_id')
        user_obj=User.objects.get(id=user_id)
        username=user_obj.username

        print("saving review")
        review.save()
        print(review.id)
        print('saved')
        return JsonResponse({'status':'success','review':review_data,'username':username,'rating':rating,'a_review_id':review.id})
    else:
        return JsonResponse({'status':"failed"})
        
def hotel_enquiry(request):
    if request.method=="POST":
        hotel_enquiry_form=HotelEnquiryForm(request.POST)
        print('in hotel enquiry')
        if hotel_enquiry_form.is_valid():
            print("form is valid")
            new_enquiry=hotel_enquiry_form.save(commit=False)

            enquired_hotel=request.POST["enquired_hotel"]
            
            hotel=Hotel.objects.get(pk=enquired_hotel)
            # manager_email=hotel.hotelmanager.email
            new_enquiry.hotel=hotel
            new_enquiry.save()

            hotel_enquiry_form.save_m2m()

            # name=hotel_enquiry_form.cleaned_data["name"]
            # email=hotel_enquiry_form.cleaned_data["email"]
            # subject=hotel_enquiry_form.cleaned_data["subject"]
            # message=hotel_enquiry_form.cleaned_data["message"]
            # phone=hotel_enquiry_form.cleaned_data["phone"]

        
            # email_from=settings.EMAIL_HOST_USER
            # email_to=manager_email
            # message_body=name+" wants to obtain some informatoin \n"+message +"\nEmail : "+email +"\nPhone : "+ phone
            # thank_subject="From "+str(hotel)
            # email_message= EmailMessage(subject,message_body, email_from, [email_to,])
            # thank_email= EmailMessage(thank_subject,"Thank you for reaching to us", email_from, [email,])
            try:
                #send email

                hotel_enquiry_form.send_enquiry_mail(hotel.id)
                # email_message.send(fail_silently=False)
                # thank_email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request,"Thanks for your Interest, We will contact you soon")
            return redirect(hotel)
        
        else:
            print("form is invalid")
            return HttpResponseRedirect('/display_hotels')


#----------Payment Methods----------#


def payment_page(request,hotel_id):
   
    
    hotel=Hotel.objects.get(pk=hotel_id)
    # book_till=datetime.strptime(request.session['book_till'],"%Y-%m-%d").date()
    # book_from=datetime.strptime(request.session['book_from'],"%Y-%m-%d").date()
    # total_days=book_till-book_from
    # date_info=pandas.Timedelta(total_days)
    # print('date_info',date_info)
    # print('days in int',type(date_info.days))
    #request.session['book_from_date']=book_from
    #request.session['book_till_date']=book_till
    # request.session['total_days']=date_info.days
    # room=hotel.rooms.filter(room_type=request.session['room_type'])
    # request.session['room_rent']=room[0].rent
    # request.session['total_bill']=int(request.session['room_count']) * int(request.session['room_rent']) * int(request.session['total_days'])
    
    
    print('in payment page',vars(request.session))
    bill_amount = request.session['total_bill']
    user = request.user
    payment_time = datetime.now()

    
    #create object but partially, extra bill be updated througourney
    order=RentPayment.objects.create(hotel=hotel,bill_amount=bill_amount,user=user,payment_time=payment_time)
    order.save()

    razorpay_client = razorpay.Client(auth=("rzp_test_JNAse3qpqKjhlQ", "DXvk6ufSfBnFBVlOkpqyxLYt"))
    

    callback_url="http://127.0.0.1:8000/handlerequest/"
    notes={"name":hotel.name,"Room Type":request.session['room_type']}
    razorpay_order=razorpay_client.order.create(dict(amount=bill_amount*100, currency='INR', notes=notes, receipt=str(order.id), payment_capture='0'))
    print(razorpay_order['id'])
    print(razorpay_order)
    order.razorpay_order_id=razorpay_order['id']
    order.save()


    context={
        'hotel': hotel,
        'order': order,
        'order_id': razorpay_order['id'],
        'callback_url':callback_url

    }    
    return render(request,"pages/booking_details_and_book.html", context)

@csrf_exempt
def handlerequest(request):
    if 'data' in request.session:
        print(vars(request.session))
    else:
        print('no data available')
    if request.method=="POST":
        razorpay_client = razorpay.Client(auth=("rzp_test_JNAse3qpqKjhlQ", "DXvk6ufSfBnFBVlOkpqyxLYt"))
        print(request.POST)
        try:
            payment_id=request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            
            try:
                order_db=RentPayment.objects.get(razorpay_order_id=order_id)
            except Exception as e:
                print(e)
                order_db.payment_status='failure'
                order_db.save()
                return HttpResponse("payment aborted")

            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            print("signature saved to database")
            order_db.save()

            result = razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
                })
            print(result)
            if result:
                print('in if loop for result')
                amount=int(order_db.bill_amount)*100
                print(amount)
                print(type(amount))
                try:
                    print('signature is valid')
                    print("proceed to capture payment")
                    hotel_id=order_db.hotel.id
                    print(hotel_id)
                    hotel=Hotel.objects.get(pk=hotel_id)
                    room_id=request.session['room_id']
                    room=Room.objects.get(pk=room_id)
                    razorpay_client.payment.capture(payment_id,amount)
                    reservation=Reservation.objects.create(room=room,user=request.user,start_date=request.session['book_from'],end_date=request.session['book_till'],payment_status='successful',created_at=datetime.now(),total_amount=request.session['total_bill'],rooms_reserved=request.session['room_count'])
                    reservation.save()

                    #room.checkout = room.checkin + timedelta(days=1)
                    #print(room.hotel.available_rooms)
                    #room.hotel.available_rooms -= 1
                    #print(room.hotel.available_rooms)
                    #room.hotel.save()
                    #room.save()
                    print("payment captured")
                    order_db.payment_status='success'
                    
                    order_db.save()
                    email_message= EmailMessage("From Hotels",f"Payment successful for ,\n \tHotel   :{room.hotel}\n \tRoom Type :{request.session['room_type']}\n \tThank You for choosing HOTELS services.\nHappy stay. ", settings.EMAIL_HOST_USER, [request.user.email])
                    email_message.send(fail_silently=False)
                    messages.success(request,f"Payment successful, please Enjoy your stay at {room.hotel}")

                    return HttpResponseRedirect("/")
                except Exception as e:
                    print(e)
                    hotel_id=order_db.hotel.id
                    
                    hotel=Hotel.objects.get(pk=hotel_id)
                    
                    order_db.payment_status='failure'
                    order_db.save()
                    messages.success(request,"Payment Failed, Please try again")

                    return redirect(hotel)
            else:

                print('signature is invalid')
                hotel_id=order_db.hotel.id
                    
                hotel=Hotel.objects.get(pk=hotel_id)
                    
                order_db.payment_status='failure'
                order_db.save()
                messages.success(request,"Razorpay signature is invalid, Payment Failed, Please try again")

                return redirect(hotel)
        except Exception as e:
            print(e)
            return HttpResponse("Not Found 505")
    else:
        return HttpResponse("You are not supposed to directly jump to this page")