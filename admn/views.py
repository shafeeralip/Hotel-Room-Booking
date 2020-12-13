from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import auth,User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from admn.models import *
import json
from django.http import JsonResponse


# Create your views here.

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_home)
    
     

    elif request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            if username =='sayi' and password =='123':
                login(request,user)
                
                return redirect(admin_home)
            else:
                messages.warning(request,'inavalid credention')
                return render(request,'admin/login.html')
        else:
            messages.warning(request,'inavalid credention')
            return render(request,'admin/login.html')
    else:
        return render(request,'admin/login.html')
          
@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def admin_home(request):
    customer = Customer.objects.all().count()
    hotels=Hoteladmin.objects.all().count()
    booking=Booking.objects.filter(complete=True,cancel=False).count()
    goahotels=Hoteladmin.objects.filter(location='GOA').count()
    benghotels=Hoteladmin.objects.filter(location='GOA').count()
    mumbaihotels=Hoteladmin.objects.filter(location='MUMBAI').count()
    kochihotels=Hoteladmin.objects.filter(location='KOCHI').count()

    context={'customer':customer,'hotels':hotels,'booking':booking,
            'goa':goahotels,'beng':benghotels,'mumbai':mumbaihotels,'kochi':kochihotels}



    

    return render(request,'admin/admin_home.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def admin_logout(request):

    logout(request)
    return render(request,'admin/login.html')

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def create_hotel(request):
    if request.method =='POST':
        username=request.POST['username']
        hotelname=request.POST['hotelname']
        password=request.POST['password']
        contactnumber=request.POST['contactnumber']
        location=request.POST['location']
        dict={'contactnumber':contactnumber,
               'hotelname':hotelname,
                'location':location,
                'username':username 
                }

        if Hoteladmin.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, 'admin/create-hotel-form.html',dict)
        else:
            user=Hoteladmin.objects.create(username=username,password=password,hotel_name=hotelname,contact=contactnumber,location=location)
          
            user.save();
            messages.info(request,'Hotel is created')
            return render(request, 'admin/create-hotel-form.html')

    return render(request, 'admin/create-hotel-form.html')

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def hotel_view(request):
    hotels=Hoteladmin.objects.all()

    return render(request,'admin/ad_hotelview.html',{'hotels':hotels})

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def hotel_edit(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    if request.method=='POST':
        hotel.hotel_name=request.POST['hotelname']
        hotel.username=request.POST['username']
        hotel.contact=request.POST['contactnumber']
        hotel.location=request.POST['location']
        hotel.password=request.POST['password']
        hotel.save();
        return redirect(hotel_view)


    return render(request,'admin/ad_hoteledit.html',{"hotel":hotel})

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def hotel_delete(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    hotel.delete()
    return redirect(hotel_view)



@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def user_view(request):
    users=User.objects.filter(is_superuser = False)
    return render(request,'admin/ad_userview.html',{'users':users})


@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def user_edit(request,id):
    user=User.objects.get(id=id)
    if request.method=='POST':
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.last_name=request.POST['contactnumber']
        user.save()
        return redirect(user_view)


    return render(request,'admin/ad_useredit.html',{'user':user})

@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def user_delete(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect(user_view)
@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def refoffer(request):
    ref=reffreal_offer.objects.all()
    return render(request,'admin/offer.html',{"ref":ref})
@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def offeredit(request,id):
    off=reffreal_offer.objects.get(id=id)
    if request.method == 'POST':
        
        offer_type=request.POST['offtype']
        off.refd_persondisc=request.POST['refpersondiscount']
        off.order_max=request.POST['ordmaximum']

        if offer_type == 'OfferByPercentage':
            off.ref_discount=request.POST['refdiscount']
            off.offer_type = offer_type

        elif offer_type == 'OfferByAmount':
            off.ref_price=request.POST['refprice']
            off.offer_type = offer_type
        
        off.save();
        return redirect(refoffer)


    return render(request,'admin/offeredit.html',{'off':off})
@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def offerstatus(request,id,value):
    off=reffreal_offer.objects.get(id=id)
    if value == 'True':
        off.ref_status=True
    elif value == 'False':
        off.ref_status=False

    off.save()
    return redirect(refoffer)


def userBlock(request,id):
  user=User.objects.get(id=id)
  if user.is_active == False:

    user.is_active = True
  else:
    
    user.is_active = False
   
  user.save()

  return redirect(user_view)


def hotelblock(request,id):
  hotel=Hoteladmin.objects.get(id=id)
  if hotel.is_active == False:

    hotel.is_active = True
  else:
    
    hotel.is_active = False
   
  hotel.save()

  return redirect(hotel_view)



def vip(request):
    viphotel=VIP.objects.filter(hotel__isnull=False)
    viproom=VIP.objects.filter(room__isnull=False)

    return render(request,'admin/vip.html',{'viphotel':viphotel,'viproom':viproom})
    
def viphotel(request):
    if request.method == "POST":
        vi=VIP.objects.filter(status=True,hotel__isnull=False).count()
        if vi < 5:
            location=request.POST['location']
            hotel_name=request.POST['hotel']
            
            hotel=Hoteladmin.objects.get(hotel_name=hotel_name,location=location)
            vip=VIP.objects.create(hotel=hotel)
            vip.save();
            return redirect('vip')
        else:
            messages.info(request,"YOU EXCEED THE HOTEL COUNT IN FRONT PAGE OF YOUR WEBSITE IF YOU WANT TO ADD YOU NEED TO DELETE OR BLOCK OTHER HOTELS")
            return render(request,'admin/adviphotel.html')



    return render(request,'admin/adviphotel.html')


def viproom(request):
    if request.method == "POST":
        vi=VIP.objects.filter(status=True,room__isnull=False).count()
        if vi < 5:
            location=request.POST['location']
            hotel_name=request.POST['hotel']
            room=request.POST['room']

            hotel=Hoteladmin.objects.get(hotel_name=hotel_name,location=location)
            rooms=Rooms.objects.get(hotel=hotel,room_type=room)

            vip=VIP.objects.create(room=rooms)
            vip.save();
            return redirect('vip')
        else:
            messages.info(request,"YOU EXCEED THE HOTEL COUNT IN FRONT PAGE OF YOUR WEBSITE IF YOU WANT TO ADD YOU NEED TO DELETE OR BLOCK OTHER HOTELS")
            return render(request,'admin/adviproom.html')
    return render(request,'admin/adviproom.html')

def location(request):
    location = request.GET['location']
    hotels=Hoteladmin.objects.values_list("hotel_name",flat=True).filter(location=location)
    
    hotel=list(hotels)
    
    return JsonResponse(hotel,safe=False)



def act(request,id,value):
    if value == 'block':
       vip= VIP.objects.get(id=id)
       if vip.status==False:
            vip.status=True
       elif vip.status==True:
            vip.status=False
            
       vip.save()
        
        
    elif value == "delete":
        VIP.objects.filter(id=id).delete()
    
    return redirect('vip')


def hotel(request):
    hotel = request.GET['hotel']
    location = request.GET['location']
    hotels=Hoteladmin.objects.get(hotel_name=hotel,location=location)

    rooms=Rooms.objects.values_list("room_type",flat=True).filter(hotel=hotels)
    
    room=list(rooms)
    
    return JsonResponse(room,safe=False)