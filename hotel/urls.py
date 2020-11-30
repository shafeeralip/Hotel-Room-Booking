from django .urls import path
from . import views


urlpatterns=[ 
    path('',views.hotel_log,name='hotel_log'),
    path('hotel-home/<int:id>/',views.hotel_home,name='hotel_home'),
    path('hotel_logout',views.hotel_logout,name='hotel_logout'),
    path('hotel_rooms/<int:id>/',views.hotel_rooms,name='hotel_rooms'),
    path('add_room/<int:id>/',views.add_room,name='add_room'),
    path('hotel_profile/<int:id>/',views.hotel_profile,name='hotel_profile'),
    path('hotel_update/<int:id>/',views.hotel_update,name='hotel_update'),
    path('room_edit/<int:id>/',views.room_edit,name='room_edit'),
    path('room_delete/<int:id>/',views.room_delete,name='room_delete'),
    path('hotel_user/<int:id>/',views.hotel_user,name='hotel_user'),
    path('hotel_booked/<int:id>/',views.hotel_booked,name='hotel_booked'),
    path('booking_detail/<int:id>/',views.booking_detail,name='booking_detail'),
        path('confirm/<int:id>/<str:value>/',views.confirm,name='confirm'),


]