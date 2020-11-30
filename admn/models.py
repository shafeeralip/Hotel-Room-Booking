from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    reff_code = models.CharField(max_length=100, null= True)
    refferd_user = models.CharField(max_length=150, null= True)


class Hoteladmin(models.Model):

    hotel_name=models.CharField(max_length=200,null=True)
    username=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=200,null=True)
    location=models.CharField(max_length=200,null=True)
    contact=models.BigIntegerField()
    description=models.TextField(max_length=1000,verbose_name='description')
    categories=models.CharField(max_length=200,null=True)
    hotelimage1=models.ImageField(null=True ,blank=True)


    @property
    def get_lowest_price(self):
        try:
            rooms =self.rooms_set.all()
            price=[]
            
            for room in rooms:
                price.append(room.room_price)
            
            lowest_price=min(price)
        except:
            lowest_price='NOT ENTERD'
        return lowest_price


    @property
    def imageURL(self):
        try:
            url= self.hotelimage1.url
        except:
            url=''
        return url
            

            

    

class Features(models.Model):
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    Free_wifi=models.BooleanField(default=False)
    Loundry_service=models.BooleanField(default=False)
    Swimming_pool=models.BooleanField(default=False)
    Restaurant=models.BooleanField(default=False)
    Parking=models.BooleanField(default=False)

class Hotel_image(models.Model):
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    image=models.ImageField(null=True ,blank=True)

class Rooms(models.Model):
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    room_type=models.CharField(max_length=200,null=True)
    # room_description=models.TextField(max_length=1000,verbose_name='description')
    sleeps=models.CharField(max_length=200,null=True)
    room_price=models.FloatField()
    room_image1=models.ImageField(null=True ,blank=True)
    room_image2=models.ImageField(null=True ,blank=True)
    room_image3=models.ImageField(null=True ,blank=True)
    room_available=models.IntegerField()


class Room_features(models.Model):
    hotel= models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    room=models.ForeignKey(Rooms,on_delete=models.SET_NULL,null=True,blank=True)
    Free_wifi=models.BooleanField(default=False)
    king_size_bed=models.BooleanField(default=False)
    TV=models.BooleanField(default=False)
    Bath_Tube=models.BooleanField(default=False)
    Safe_box=models.BooleanField(default=False)
    Welcome_bottle=models.BooleanField(default=False)
    Breakfast=models.BooleanField(default=False)
    Lunch=models.BooleanField(default=False)
    Dinner=models.BooleanField(default=False)
    

class Room_image(models.Model):
    room=room=models.ForeignKey(Rooms,on_delete=models.SET_NULL,null=True,blank=True)
    image=models.ImageField(null=True ,blank=True)




class Booking(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    date_booked=models.DateField(auto_now=True)
    check_in=models.DateField(null=True,blank=True)
    check_out=models.DateField(null=True,blank=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    total_price=models.BigIntegerField(default=0,null=True,blank=True)
    payment_status=models.CharField(max_length=200,null=True)
    total_guest=models.CharField(max_length=200,null=True)
    cancel=models.BooleanField(default=False,null=True,blank=True)
    confirm=models.BooleanField(default=False,null=True,blank=True)
    
    @property
    def total_rooms(self):
        roombooked=self.roombooked_set.all()
        total=sum(room.quantity for room in roombooked)
        return total
        

class Roombooked(models.Model):
    room=models.ForeignKey(Rooms,on_delete=models.SET_NULL,null=True,blank=True)
    booking=models.ForeignKey(Booking,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)
    

    @property
    def get_total(self):
        total = self.room.room_price * self.quantity
        return total




class reffreal_offer(models.Model):
    ref_name = models.CharField(null = True, max_length=225)
    ref_discount = models.IntegerField(null = True)
    ref_price = models.IntegerField(null = True)
    referd_person_discount = models.IntegerField(null = True)
    order_maximum = models.IntegerField(null = True)
    ref_status = models.BooleanField(null=True,default=True)
    offer_type=models.CharField(max_length=200,null=True)











