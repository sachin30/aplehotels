# from django.db.models.signals import post_save
# from django.contrib.auth.models import User,Group
# from hotel.models import Hotel
# from room.models import Room
# from django.db.models import F


# def total_rooms_adjust(sender, instance , created, **kwargs):
#     if created:
#         print("total room created")

#         if instance.hotel.total_rooms == None :
#             print("initializing available room number")
#             instance.hotel.total_rooms = 1
#             instance.hotel.save()
#         else:
#             instance.hotel.total_rooms =F('total_rooms') + 1
#             instance.hotel.save()
#             print("Number of total rooms increased")
#     else:
#         total_rooms=Room.objects.filter(hotel=instance.hotel)
#         print(len(total_rooms))
#         instance.hotel.total_rooms=len(total_rooms)
#         instance.hotel.save()

        

# post_save.connect(total_rooms_adjust,sender=Room)

# def available_rooms_adjust(sender,instance,created,**kwargs):
#     if created:
#         print("available room created")
#         if instance.hotel.available_rooms == None or instance.hotel.available_rooms == '':
#             print("initializing available room number")
#             instance.hotel.available_rooms= 1
#             instance.hotel.save()
#         else:
#             instance.hotel.available_rooms = F('available_rooms') + 1
#             instance.hotel.save()
#             print("Number of available rooms increased")
#     else:
#         print("available room already present")
#         available_rooms=Room.objects.filter(booking_status='available',hotel=instance.hotel)
#         print(len(available_rooms))
#         instance.hotel.available_rooms=len(available_rooms)
#         instance.hotel.save()
        
# post_save.connect(available_rooms_adjust,sender=Room)


    

# def assign_group_to_user(sender, instance , created, **kwargs):
#     if created:
#         group= Group.objects.get(name="customer")    
#         instance.groups.add(group)
#     print("User is assigned to customer group via signal functionality")

# post_save.connect(assign_group_to_user,sender=User)

# # def available_rooms_decrease(sender,instance,created,**kwargs):
# #     if created:
# #         print("available room deleted")
# #         if instance.hotel.available_rooms == None or instance.hotel.available_rooms == '':
# #             print("initializing available room number")
# #             instance.hotel.available_rooms= 1
# #             instance.hotel.save()
# #         else:
# #             instance.hotel.available_rooms = F('available_rooms') + 1
# #             instance.hotel.save()
# #             print("Number of available rooms increased")
# #     else:
# #         print("available room already present")
# #         available_rooms=Room.objects.filter(booking_status='available',hotel=instance.hotel)
# #         print(len(available_rooms))
# #         instance.hotel.available_rooms=len(available_rooms)
# #         instance.hotel.save()
        
# # post_save.connect(available_rooms_adjust,sender=Room)
