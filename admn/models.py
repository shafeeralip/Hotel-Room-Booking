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
    hotelimage2=models.ImageField(null=True ,blank=True)
    hotelimage3=models.ImageField(null=True ,blank=True)

class Features(models.Model):
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    feature=models.CharField(max_length=200,null=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)

class Rooms(models.Model):
    hotel=models.ForeignKey(Hoteladmin,on_delete=models.SET_NULL,null=True,blank=True)
    room_name=models.CharField(max_length=200,null=True)
    room_description=models.TextField(max_length=1000,verbose_name='description')
    room_type=models.CharField(max_length=200,null=True)
    room_price=models.FloatField()
    room_image1=models.ImageField(null=True ,blank=True)
    room_image2=models.ImageField(null=True ,blank=True)
    room_image3=models.ImageField(null=True ,blank=True)










