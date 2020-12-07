from django .urls import path
from . import views


urlpatterns=[

    path('',views.home,name='home'),
    path('login',views.user_login,name="user_login"),
    path('mobail',views.mobile_login,name="mobile_login"),
    path('otp_generate',views.otp_generate,name='otp_generate'),
    path('register_user',views.register_user,name='register_user'),
    path('logout',views.user_logout,name="user_logout"),
    path('hotel-view/<int:id>/',views.hotel_view,name="hotel_view"),
    path('booking/<int:id>/',views.booking,name="booking"),
    path('hotel_list/<str:city>/',views.hotel_list,name='hotel_list'),
    path('booking_details/',views.booking_details,name='booking_details'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('report/<int:id>/<str:pay>/',views.report,name='report'),
    path('reffral_signup/<str:referalcode>/',views.reffral_signup,name='reffral_signup'),
    path('search',views.search,name='search'),
    path('guestreg',views.guestreg,name='guestreg')


    
    

]