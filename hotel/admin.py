from django.contrib import admin
from admn.models import *

# Register your models here
class Hotels(admin.ModelAdmin):
    list_display=('hotel_name','username','location','contact','categories','hotelimage1')

class Customers(admin.ModelAdmin):
    list_display=('user','name','email','reff_code','refferd_user')

admin.site.register(Hoteladmin,Hotels)
admin.site.register(Rooms)
admin.site.register(Features)
admin.site.register(Room_features)

admin.site.register(Hotel_image)
admin.site.register(Room_image)
admin.site.register(Booking)
admin.site.register(Roombooked)
admin.site.register(Customer,Customers)
admin.site.register(reffreal_offer)

