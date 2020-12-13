from django .urls import path
from . import views


urlpatterns=[ 
    path('',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('create_hotel',views.create_hotel,name='create_hotel'),
    path('hotel_view',views.hotel_view,name='hotel_view'),
    path('hotel_edit/<int:id>/',views.hotel_edit,name='hotel_edit'),
    path('hotel_delete/<int:id>/',views.hotel_delete,name='hotel_delete'),
    path('user_view',views.user_view,name='user_view'),
    path('user_edit/<int:id>/',views.user_edit,name='user_edit'),
    path('user_delete/<int:id>/',views.user_delete,name='user_delete'),
    path('refoffer',views.refoffer,name='refoffer'),
    path('offeredit/<int:id>/',views.offeredit,name='offeredit'),
    path('offerstatus/<int:id>/<str:value>/',views.offerstatus,name='offerstatus'),
    path('userBlock/<int:id>/',views.userBlock,name='userBlock'),
    path('hotelblock/<int:id>/',views.hotelblock,name='hotelblock'),
    path('vip',views.vip,name='vip'),
    path('viphotel',views.viphotel,name='viphotel'),
    path('viproom',views.viproom,name='viproom'),
    path('location',views.location,name='location'),
   path('hotel',views.hotel,name='hotel'),
    path('act/<int:id>/<str:value>/',views.act,name='act'),



]