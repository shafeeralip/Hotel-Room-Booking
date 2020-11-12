from django .urls import path
from . import views


urlpatterns=[

    path('',views.home,name='home'),
    path('login',views.user_login,name="user_login"),
    path('mobail',views.mobile_login,name="mobile_login"),
    path('otp_generate',views.otp_generate,name='otp_generate'),
    path('register_user',views.register_user,name='register_user'),
    path('logout',views.user_logout,name="user_logout"),
    path('hotel-view',views.hotel_view,name="hotel_view"),
    path('booking',views.booking,name="booking"),
    path('hotel_list',views.hotel_list,name='hotel_list')


    
    

]