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
from django.core.files.storage import FileSystemStorage
from datetime import date
# Create your views here.

def hotel_log(request):
    global id
    if "hotel" in request.session:

        return redirect(hotel_home,id=id)

    elif request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if Hoteladmin.objects.filter(username=username,password=password).exists():
            hotel_admin=Hoteladmin.objects.get(username=username,password=password)
            print(hotel_admin)
            hotelname=hotel_admin.id
            
            id=hotel_admin.id
            request.session['hotel']=hotelname
            return redirect(hotel_home,id=hotelname)

        else:
            messages.warning(request,'inavalid credention')
            return render(request,'hotel/hotel-login.html')

    
    return render(request,'hotel/hotel-login.html')

@custom_decorator
def hotel_home(request,id):

    hotel=Hoteladmin.objects.get(id=id)
    today=date.today()
    todaybooking=Booking.objects.filter(hotel=hotel,complete=True,date_booked=today)
    booking=Booking.objects.filter(hotel=hotel,complete=True)
    bookcount=booking.count()
    todaybookcount=todaybooking.count()
    customers=[]
    for book in booking:
        if book.customer.name not in customers:
            customers.append(book.customer.name)
    
    customerscount=len(customers)

    today_income=0
    for todaybook in todaybooking:
        today_income=today_income + todaybook.total_price
    
    total_income=0

    for book in booking:
        total_income=total_income + book.total_price

    
    total_rooms=Rooms.objects.filter(hotel=hotel).count()

    context={'hotel':hotel,'todayinc':today_income,'totalinc':total_income,'totalroom':total_rooms,
            'todaybook':todaybookcount,'totalbook':bookcount,'customer':customerscount}


   

    if request.session.get('hotel') is None:
        return redirect(hotel_log)
    else:
        return render(request,'hotel/hotel-home.html',context)



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
    rooms=Rooms.objects.filter(hotel=hotel)
    
    context={'hotel':hotel,
                'rooms':rooms}


    return render(request,'hotel/hotel-rooms.html',context)
@custom_decorator
def add_room(request,id):

    hotel=Hoteladmin.objects.get(id=id)

    if request.method=='POST':
        room_type=request.POST['room_type']
        sleeps=request.POST['sleeps']
        room_price=request.POST['room_price']
        available_room=request.POST['available_room']
        # room_description=request.POST['room_description']
       
        features=request.POST.getlist('features')
        food=request.POST.getlist('food')
        images=request.FILES.getlist('file[]')

       


        room=Rooms.objects.create(hotel=hotel,room_type=room_type,sleeps=sleeps,
                                    room_price=room_price,room_available=available_room)
        
        room.save();
        room_features=Room_features.objects.create(hotel=hotel,room=room)
       

        for feature in features:
            if feature == 'Free_wifi':
                room_features.Free_wifi = True
                break
            else:
                room_features.Free_wifi = False
        for feature in features:

            if feature =='king_size_bed':
                room_features.king_size_bed = True
                break
            else:
                room_features.king_size_bed = False

        for feature in features:

            if feature=='TV':
                room_features.TV = True
                break
            else:
                room_features.TV = False

        for feature in features:
            
            if feature=='Bath_Tube':
                room_features.Bath_Tube = True
                break
            else:
                room_features.Bath_Tube = False
        for feature in features:

            if feature=='Safe_box':
                room_features.Safe_box = True
                break
            else:
                room_features.Safe_box = False

        for feature in features:

            if feature=='Welcome_bottle':
                room_features.Welcome_bottle = True
                break
            else:
                room_features.Welcome_bottle = False
        
            
        for food in food:

            if food=='Breakfast':
                room_features.Breakfast = True
                break
            else:
                room_features.Breakfast = False
        
        for food in food:

            if food=='Lunch':
                room_features.Lunch = True
                break
            else:
                room_features.Lunch = False

        for food in food:

            if food=='Dinner':
                room_features.Dinner = True
                break
            else:
                room_features.Dinner = False

           
           
        room_features.save();

        for image in images:
            fs=FileSystemStorage()
            file_path=fs.save(image.name,image)
            room_image=Room_image(room=room,image=file_path)
            room_image.save();

            
        messages.info(request,'ROOM is saved')
        return render(request,'hotel/room-add.html',{'hotel':hotel})
        

    return render(request,'hotel/room-add.html',{'hotel':hotel})

@custom_decorator
def hotel_profile(request,id):
    
    hotel=Hoteladmin.objects.get(id=id)
    hotel_features,created =Features.objects.get_or_create(hotel=hotel)
    features=[]
    if hotel_features.Free_wifi == True:
        features.append("FREE Wifi")
    if hotel_features.Loundry_service==True:
        features.append("Loundry Service")
    if hotel_features.Swimming_pool==True:
        features.append("Swimming Pool")
    if hotel_features.Restaurant==True:
        features.append("Restaurant")
    if hotel_features.Parking==True:
        features.append("Parking")
    
    print(features)
    context={'features':features,'hotel':hotel}



    return render(request,'hotel/hotel_profile.html',context)

@custom_decorator
def hotel_update(request,id):
    
    hotel=Hoteladmin.objects.get(id=id)
    


    hotel_image=Hotel_image.objects.filter(hotel=hotel)
  

  
    if Features.objects.filter(hotel=hotel).exists():

        hotel_features = Features.objects.filter(hotel=hotel)[0]
    else:

        hotel_features = Features.objects.create(hotel=hotel)

    print("hotel",hotel_image)

    



    
    if request.method=='POST':
        hotel.hotel_name=request.POST['hotel_name']
        hotel.location=request.POST['hotel_location']
        hotel.contact=request.POST['hotel_contact']
        hotel.categories=request.POST['hotel_category']
        hotel.description=request.POST['hotel_description']
        featurs=request.POST.getlist('features')

        for feature in featurs:
            if feature == 'Loundry_service':
                hotel_features.Loundry_service = True
                break
            else:
                hotel_features.Loundry_service = False

        for feature in featurs:
            if feature =='Swimming_pool':
                hotel_features.Swimming_pool = True
                break
            else:
                hotel_features.Swimming_pool = False

        for feature in featurs:

            if feature=='Restaurant':
                hotel_features.Restaurant = True
                break
            else:
                hotel_features.Restaurant = False

        for feature in featurs:

            if feature=='Parking':
                hotel_features.Parking = True
                break
            else:
                hotel_features.Parking = False

        for feature in featurs:

            if feature=='Free_wifi':
                hotel_features.Free_wifi = True
                break
            else:
                hotel_features.Free_wifi = False


        hotel_features.save()
            


        if 'image1' not in request.POST:
            hotel.hotelimage1=request.FILES.get('image1')
        
           

        else:
           hotel.hotelimage1=hotel.hotelimage1

        

        images=request.FILES.getlist('file[]')
        for image in images:
            fs=FileSystemStorage()
            file_path=fs.save(image.name,image)
            hotel_image=Hotel_image(hotel=hotel,image=file_path)
            hotel_image.save()

       
            
        
          
        hotel.save()
        
        return redirect(hotel_profile,id=hotel.id)
    context={'hotel':hotel,'hotel_feature':hotel_features,'hotel_image':hotel_image}




    return render(request,'hotel/hotel_update.html',context)


@custom_decorator
def room_edit(request,id):
    room=Rooms.objects.get(id=id)
    room_images=Room_image.objects.filter(room=room)
    room_features=Room_features.objects.get(room=room)
    if request.method=='POST':
        room.room_type=request.POST['room_type']
        room.sleeps=request.POST['sleeps']
        room.room_price=request.POST['room_price']
        room.room_available=request.POST['available_room']
        features=request.POST.getlist('features')
        print(features)
        images=request.FILES.getlist('file[]')


        for feature in features:
            if feature == 'Free_wifi':
                room_features.Free_wifi = True
                break
            else:
                room_features.Free_wifi = False
        for feature in features:

            if feature =='king_size_bed':
                room_features.king_size_bed = True
                break
            else:
                room_features.king_size_bed = False

        for feature in features:

            if feature=='TV':
                room_features.TV = True
                break
            else:
                room_features.TV = False

        for feature in features:
            
            if feature=='Bath_Tube':
                room_features.Bath_Tube = True
                break
            else:
                room_features.Bath_Tube = False
        for feature in features:

            if feature=='Safe_box':
                room_features.Safe_box = True
                break
            else:
                room_features.Safe_box = False

        for feature in features:

            if feature=='Welcome_bottle':
                room_features.Welcome_bottle = True
                break
            else:
                room_features.Welcome_bottle = False
            

        foods=request.POST.getlist('food')
        print(foods)

        for food in foods:

            if food=='Breakfast':
                room_features.Breakfast = True
                break
            else:
                room_features.Breakfast = False
        
        for food in foods:

            if food =='Lunch':
                room_features.Lunch = True
                break
            else:
                room_features.Lunch = False

        for food in foods:

            if food == 'Dinner':
                room_features.Dinner = True
                break
            else:
                room_features.Dinner = False

           
           
        room_features.save();


        for image in images:
            fs=FileSystemStorage()
            file_path=fs.save(image.name,image)
            room_image=Room_image(room=room,image=file_path)
            room_image.save();




       
        # if 'image1' not in request.POST:
        #     room.room_image1=request.FILES.get('image1')
           
             

        # else:
        #    room.room_image1=room.room_image1
        # if 'image2' not in request.POST:
        #     room.room_image2=request.FILES.get('image2')
                
                    

        # else:
        #     room.room_image2=room.room_image2
        
        # if 'image3' not in request.POST:
        #     room.room_image3=request.FILES.get('image3')
                
                    

        # else:
        #     room.room_image3=room.room_image3


        room.save();
        
        return redirect(hotel_rooms,id=room.hotel.id)
    

    context={'room':room,'room_images':room_images,'room_feature':room_features}
         

    return render(request,'hotel/room_edit.html',context)
    

@custom_decorator
def room_delete(request,id):
    room=Rooms.objects.get(id=id)
    room.delete()
    return redirect(hotel_rooms,id=room.hotel.id)



@custom_decorator
def hotel_user(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    booking=Booking.objects.filter(hotel=hotel)
    
    customers=[]
    dictionary=dict()
    dif=dict()
    name=[]
    email=[]



    for book in booking:
        
        if book.customer.name in dictionary:
            dictionary[book.customer.name] +=1
        else:
            dictionary[book.customer.name]=1

    for book in booking:
        if book.customer.name not in name:
            name.append(book.customer.name)
            email.append(book.customer.email)



    for i in range(len(email)):
        dif={'name':name[i],
                    'email':email[i],
                    'booking':dictionary[name[i]]
                    }
        customers.append(dif)
    
    context={'hotel':hotel,'customers':customers}
                    
            
    return render(request,'hotel/hotel_customer.html',context)

    

@custom_decorator
def hotel_booked(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    booking=Booking.objects.filter(hotel=hotel,complete=True,cancel=False).order_by('-check_in')



    context={'hotel':hotel,'booking':booking}
    return render(request,'hotel/hotel_booked.html',context)


@custom_decorator
def booking_detail(request,id):
    booking=Booking.objects.get(id=id)
    date=booking.check_out - booking.check_in
    context={"booking":booking,'date':date}
    return render(request,'hotel/booking_detailed.html',context)

def confirm(request,id,value):
    booking=Booking.objects.get(id=id)
    if value == 'cancel':
        booking.cancel = True
    elif value == 'confirm':
        booking.confirm = True
    
    booking.save()

    return redirect(hotel_booked,id=booking.hotel.id)



