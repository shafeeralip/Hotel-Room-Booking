from django.db import models

# Create your models here.

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












