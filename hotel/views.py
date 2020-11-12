from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from admn.models import *
from user.views import *
from .decorators import custom_decorator
from django.core.files import File
from django.core.files.base import ContentFile
# Create your views here.

def hotel_log(request):
    if "hotel" in request.session:

        return redirect(home)

    elif request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if Hoteladmin.objects.filter(username=username,password=password).exists():
            hotel_admin=Hoteladmin.objects.get(username=username,password=password)
            print(hotel_admin)
            hotelname=hotel_admin.id
            request.session['hotel']=hotelname
            return redirect(hotel_home,id=hotelname)

        else:
            messages.warning(request,'inavalid credention')
            return render(request,'hotel/hotel-login.html')

    
    return render(request,'hotel/hotel-login.html')

@custom_decorator
def hotel_home(request,id):

    hotel=Hoteladmin.objects.get(id=id)

   

    if request.session.get('hotel') is None:
        return redirect(hotel_log)
    else:
        return render(request,'hotel/hotel-home.html',{'hotel':hotel})


   
    
        



@custom_decorator
def hotel_logout(request):
    if request.session.get('hotel') is None:
        return redirect(hotel_log)
    else:
        request.session.flush()
        return render(request,'hotel/hotel-login.html')

       
        # del request.session['hotel']
       
        
       

    # if "hotel" in request.session:
    #     del request.session['hotel']
    #     return render(request,'hotel/hotel-login.html')
    # else:
    #     return redirect(hotel_log)

@custom_decorator
def hotel_rooms(request,id):

    hotel=Hoteladmin.objects.get(id=id)

    return render(request,'hotel/hotel-rooms.html',{'hotel':hotel})
@custom_decorator
def add_room(request,id):
    hotel=Hoteladmin.objects.get(id=id)

    return render(request,'hotel/room-add.html',{'hotel':hotel})
@custom_decorator
def hotel_profile(request,id):
    
    hotel=Hoteladmin.objects.get(id=id)

    return render(request,'hotel/hotel_profile.html',{'hotel':hotel})
@custom_decorator
def hotel_update(request,id):
    
    hotel=Hoteladmin.objects.get(id=id)


    
    if request.method=='POST':
        hotel.hotel_name=request.POST['hotel_name']
        hotel.location=request.POST['hotel_location']
        hotel.contact=request.POST['hotel_contact']
        hotel.categories=request.POST['hotel_category']
        hotel.description=request.POST['hotel_description']
        if 'image1' not in request.POST:
            hotel.hotelimage1=request.FILES.get('image1')
           
             

        else:
           hotel.hotelimage1=hotel.hotelimage1
        if 'image2' not in request.POST:
            hotel.hotelimage2=request.FILES.get('image2')
                
                    

        else:
            hotel.hotelimage2=hotel.hotelimage2
        
        if 'image3' not in request.POST:
            hotel.hotelimage3=request.FILES.get('image3')
                
                    

        else:
            hotel.hotelimage3=hotel.hotelimage3
         
            
        
          
        hotel.save();
        
        return redirect(hotel_profile,id=hotel.id)








    return render(request,'hotel/hotel_update.html',{'hotel':hotel})