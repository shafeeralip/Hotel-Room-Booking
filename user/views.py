from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
import requests
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from admn.models import *
import razorpay
import string
import random
import re
# Create your views here.




def home(request):
    if request.method=='POST':

        user=request.user
        name=request.user.username
        email=request.user.email
        customer,created =Customer.objects.get_or_create(user=user,name=name,email=email)
    
    return render(request,'user/index.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect(home)

    elif request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(home)
        else:
            dicti={'error':"inavlid credention"}
            return render(request,'user/user_login.html',dicti)
    else:
        return render(request,'user/user_login.html')

    return render(request,'user/user_login.html')


def user_logout(request):
        logout(request)
        return redirect(home)

def otp_generate(request):

    value = json.loads(request.body)
    mobile = value['mobile']
    print("mobai",mobile)

    mobile=str(91) + mobile


    url = "https://d7networks.com/api/verifier/send"

    payload = {'mobile': mobile,
    'sender_id': 'SMSINFO',
    'message': 'Your otp code is {code}',
    'expiry': '900'}
    files = [

    ]
    headers = {
    'Authorization': 'Token 530907b026ae0c827d992f6842a80273b1656205'
    }

    response = requests.request("POST", url, headers=headers, data = payload, files = files)

    print(response.text.encode('utf8'))

    data=response.text.encode('utf8')
    datadict=json.loads(data.decode('utf-8'))

    id=datadict['otp_id']
    status=datadict['status']
    print('id:',id)
    request.session['id'] = id


    return JsonResponse('item was added',safe=False)



def register_user(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        number=request.POST['mobile']
        # otp=request.POST['otp']
        dicti = {"username":username,"email":email,"mobile":number}
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, "user/user_login.html", dicti)
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request, "user/user_login.html", dicti)
        elif User.objects.filter(last_name=number).exists():
            messages.info(request,'mobail number already taken')
            return render(request, "user/user_login.html", dicti)
        else:
            # id=request.session['id']
            # url = "https://d7networks.com/api/verifier/verify"

            # payload = {'otp_id': id,
            # 'otp_code': otp}
            # files = [

            # ]
            # headers = {
            # 'Authorization': 'Token 530907b026ae0c827d992f6842a80273b1656205'
            # }

            # response = requests.request("POST", url, headers=headers, data = payload, files = files)

            # print(response.text.encode('utf8'))
            # data=response.text.encode('utf8')
            # datadict=json.loads(data.decode('utf-8'))
            # status=datadict['status']
            
            # if status=='success':

            
            letter = string.ascii_letters
            result = ''.join(random.choice(letter) for i in range(8))
            user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
            customer=Customer.objects.create(user=user,name=username,email=email,reff_code=result)
            user.save();
            customer.save();

            login(request,user,backend='django.contrib.auth.backends.ModelBackend')

            return redirect(home)

            # else:
               
            #     messages.info(request,'incorrect otp')
            #     return render(request,'user/user_login.html')
    return render(request,'user/user_login.html')



def mobile_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method =='POST':
        mobile=request.POST['mobile']
        otp=request.POST['otp']
        if User.objects.filter(last_name=mobile).exists():
            user=User.objects.get(last_name=mobile)
            print(user)
            username = user.username
            password=user.first_name
            id=request.session['id']
            url = "https://d7networks.com/api/verifier/verify"

            payload = {'otp_id': id,
            'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token 530907b026ae0c827d992f6842a80273b1656205'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))
            status=datadict['status']
            
            if status=='success':
                user=authenticate(username=username,password=password)
             
                login(request,user)
                return redirect(home)
            else:
                dicti={'error':"inavlid OTP"}
                return render(request,'user/mobile_login.html',dicti)

        else:

            messages.info(request,'mobail is not registerd')
            return render(request,'user/mobile_login.html')

    
    return render(request,'user/mobile_login.html')



    

def hotel_view(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    rooms=Rooms.objects.filter(hotel=hotel)
    if request.user.is_authenticated:

        customer=request.user.customer
        print("hello",customer,hotel)
        if Booking.objects.filter(customer=customer,hotel=hotel,complete=False).exists():

            booking=Booking.objects.get(customer=customer,hotel=hotel,complete=False)
            print("helloo" ,booking)
            
            guest = booking.total_guest
        
            roombooked=Roombooked.objects.filter(booking=booking)
            print(roombooked)
            date=booking.check_out - booking.check_in
            checkindate =str(booking.check_in.month)  +"-"+str(booking.check_in.day) +"-"+str(booking.check_in.year) 
            checkoutdate =str(booking.check_out.month)  +"-"+str(booking.check_out.day) +"-"+str(booking.check_out.year) 
            print("hi ",checkindate)
        


            context={'hotel':hotel,'rooms':rooms,'booking':booking,'checkin':checkindate,'checkout':checkoutdate,'date':date,'roombooked':roombooked,'guest':guest}
            return render(request,'user/hotel_view.html',context)
    try:

        checkin=request.session['checkin']
        checkout=request.session['checkout']
        guest=request.session['guest']
    except:
        checkin=''
        checkout=''
        guest=''

    context={'hotel':hotel,'rooms':rooms,'checkin':checkin,'checkout':checkout,'guest':guest}
    return render(request,'user/hotel_view.html',context)
    


def booking(request,id):
    hotel=Hoteladmin.objects.get(id=id)
    rooms=Rooms.objects.filter(hotel=hotel) 
   

    
    if request.method =='POST':
       
        check_out=request.POST.get('checkout')
        
        try:
            check_in=request.POST['checkin']
           
        except:
            pass

        
        total_guest=request.POST['adults']
       

        if check_in == ''  or total_guest == '0' :
            
            messages.info(request,"please fill details and select rooms")
            context={'hotel':hotel,'rooms':rooms}

            return redirect(hotel_view,id=id)

        
    if request.user.is_authenticated:


        user = User.objects.get(username=request.user.username)
        ref=reffreal_offer.objects.all()
        booktotal=0
        prev_book=''
    
        customer=Customer.objects.get(user=user)
        
        
        booking=Booking.objects.get(hotel=hotel,customer=customer,complete=False)
        if customer.refferd_user:

            if Booking.objects.filter(customer=customer,complete=True).exists():
                prev_book=True
                booktotal = booking.total_price
            else:
                prev_book=False
                for off in ref:
                    if off.offer_type == 'OfferByPercentage' :
                        booktotal=booking.total_price * (off.ref_discount/100)
                        

                    elif off.offer_type == 'OfferByAmount':
                        booktotal=booking.total_price - off.ref_price
        else:
            booktotal = booking.total_price

            
    
        bookedrooms=booking.roombooked_set.all()
        

        date= booking.check_out - booking.check_in
        for bkroom in bookedrooms:
            images=bkroom.room.room_image_set.all()
            for image in images:
                image=image.image
                break 
    

        client=razorpay.Client(auth=("rzp_test_7i01eG7knm1628","K9H5VQX0OHOsFwPMDY8DCMzp"))
        order_currency='INR'
        order_receipt = 'order-rctid-11'
        totalprice=booktotal * 100

        response = client.order.create(dict(
            amount=totalprice,
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='0'
        
        ))
        order_id=response['id']

        bookdetails={'booking':booking,'rooms':bookedrooms,'date':date,'order_id':order_id,'booktotal':booktotal,'ref':ref,'prev_book':prev_book}

        return render(request,'user/booking.html',bookdetails)
    else:
        
        booking_rooms=request.COOKIES['booking-details'] 
        book_details = list(eval(booking_rooms))
        
        print("hiiiiilooooo",book_details)
        
        rooms=[]
        hotel=''
        total_price=''
        total_guest=''
        total_rooms=0
        total_days=''
        checkin = ''
        checkout = ''
        dic={}
        roomscount=[]

        for booking_details in book_details:


            room = Rooms.objects.get(id =int(booking_details['roomid']))
            rooms.append(room)
            dic['room']=room
            dic['count']=booking_details['roomscount']
            roomscount.append(dic)
            hotel = Hoteladmin.objects.get(id=int(booking_details['hotelid']))
            total_price = booking_details['totalprice']
            total_guest = booking_details['totalguest']
            total_rooms +=1
            total_days = booking_details['totaldays']
            checkin = booking_details['checkin']
            checkout = booking_details['checkout']



        zippedList = zip(rooms,roomscount)

        client=razorpay.Client(auth=("rzp_test_7i01eG7knm1628","K9H5VQX0OHOsFwPMDY8DCMzp"))
        order_currency='INR'
        order_receipt = 'order-rctid-11'
        totalprice= int(total_price) * 100

        response = client.order.create(dict(
            amount=totalprice,
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='0'
        
        ))
        order_id=response['id']

        
        context={'hotel':hotel,'total_price':total_price,'total_guest':total_guest,'total_rooms':total_rooms,'total_days':total_days,'checkin':checkin,'checkout':checkout,'rooms':rooms,'zip':zippedList,'order_id':order_id}

        return render(request,'user/booking.html',context)






    return render(request,'user/booking.html')
    

    


def hotel_list(request,city):
    city_name=city
    hotels= Hoteladmin.objects.filter(location=city)
    try:

        location=request.session['location']
        checkin=request.session['checkin']
        checkout=request.session['checkout']
        guest=request.session['guest']
    except:
        location = ''
        checkin = ''
        checkout = ''
        guest = ''


    print("helloo",location)

    bla='hellooo'

    
    
    context={'city_name':city_name,'hotels':hotels,'location':location,'checkin':checkin,'checkout':checkout,'guest':guest,'bla':bla}



    return render (request,'user/hotel_listing.html',context)



def booking_details(request):
    value = json.loads(request.body)
    room_details=value['room_detail']
    booking_rooms=[]
    for room_detail in room_details:
        
        if int(room_detail['roomscount']) > 0:
            booking_rooms.append(room_detail)
    print("hello",booking_rooms)
    
    if request.user.is_authenticated:
        user=request.user
        username=request.user.username
        email=request.user.email

        
        customer,created =Customer.objects.get_or_create(user=user,name=username,email=email)
        for booking_room in booking_rooms:
            print(booking_room)
            hotel=Hoteladmin.objects.get(id=int(booking_room['hotelid']))
            room=Rooms.objects.get(id=int(booking_room['roomid']))
            print('date',booking_room['checkin'])
            checkindates=booking_room['checkin'].split("-")
            checkin=checkindates[2]+"-"+checkindates[0]+"-"+checkindates[1]
            checkoutdates=booking_room['checkout'].split("-")
            checkout=checkoutdates[2]+"-"+checkoutdates[0]+"-"+checkoutdates[1]


            booking,created=Booking.objects.get_or_create(customer=customer,hotel=hotel,complete=False)
            booking.total_price=int(booking_room['totalprice'])
            booking.check_in=checkin
            booking.check_out=checkout
            booking.total_guest=booking_room['totalguest']
            roombooked,created=Roombooked.objects.get_or_create(booking=booking,room=room)
            roombooked.quantity=int(booking_room['roomscount'])
            booking.save()
            roombooked.save()
        return JsonResponse('items created' ,safe=False)
    
    else:
        response = JsonResponse('items created' ,safe=False)
        response.set_cookie('booking-details',booking_rooms) 
        

        
    
    return response


def user_profile(request):
    customer=request.user.customer
    off_type=''
    value=''
    total_referd=Customer.objects.filter(refferd_user=customer.name).count()
    ref=reffreal_offer.objects.all()
    for off in ref:
        wallet= total_referd * off.referd_person_discount
       
            
    
    if Booking.objects.filter(customer=customer).exists():
        value=False
    else:
        if customer.refferd_user:
           value=True
           

        

    print("cc",booking)

    return render(request,'user/useraccount.html',{'customer':customer,'wallet':wallet,'value':value,'ref':ref})


def report(request,id,pay):
    print(pay)
    booking=Booking.objects.get(id=id)
    date=booking.check_out - booking.check_in
    if request.method =='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
    if request.user.is_authenticated:
        booking.complete=True
        booking.confirm = True
       
       

        if pay=='COD':
            booking.payment_status='Pay at hotel'
        elif pay=='RAZOR':
            booking.payment_status='RAZORPAY'
        elif pay== 'PAY':
            booking.payment_status='PAYPAL'

        booking.save();
    ref=reffreal_offer.objects.all()
    if Booking.objects.filter(id=id,complete=True).exists():
        prev_book=True
        booktotal = booking.total_price
    else:
        prev_book=False
        for off in ref:
            if off.offer_type == 'OfferByPercentage' :
                booktotal=booking.total_price * (off.ref_discount/100)

            elif off.offer_type == 'OfferByAmount':
                booktotal=booking.total_price - off.ref_price


    context={"booking":booking,'date':date,'ref':ref,'booktotal':booktotal,'prev_book':prev_book}
    
    return render(request,'user/report.html',context)

def reffral_signup(request,referalcode):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        number=request.POST['mobile']
        # otp=request.POST['otp']
        dicti = {"username":username,"email":email,"mobile":number,'refcode':referalcode}
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, "user/referalreg.html", dicti)
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request, "user/referalreg.html", dicti)
        elif User.objects.filter(last_name=number).exists():
            messages.info(request,'mobail number already taken')
            return render(request, "user/referalreg.html", dicti)
        else:
            letter = string.ascii_letters
            result = ''.join(random.choice(letter) for i in range(8))
            if Customer.objects.filter(reff_code=referalcode).exists():
                
                ref_user=Customer.objects.get(reff_code=referalcode)
                user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
                customer=Customer.objects.create(user=user,name=username,email=email,reff_code=result,refferd_user=ref_user.name)

                user.save();
                customer.save();

                login(request,user,backend='django.contrib.auth.backends.ModelBackend')

                return redirect(home)
            else:
               
                messages.info(request,'Not a valid referral Id')
                return render(request,'user/referalreg.html',dicti)



    return render(request,'user/referalreg.html',{'refcode':referalcode})


def search(request):
    if request.method == 'POST':
        location = request.POST['location']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        guest = request.POST['guest']

        request.session['location'] = location
        request.session['checkin'] = checkin
        request.session['checkout'] = checkout
        request.session['guest'] = guest

        return redirect(hotel_list,city=location)

def guestreg(request):
    if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        number=request.POST['mobile']
        # otp=request.POST['otp']
        dicti = {"username":username,"email":email,"mobile":number}
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, "user/booking.html", dicti)
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request, "user/booking.html", dicti)
        elif User.objects.filter(last_name=number).exists():
            messages.info(request,'mobail number already taken')
            return render(request, "user/booking.html", dicti)
        else:
            letter = string.ascii_letters
            result = ''.join(random.choice(letter) for i in range(8))
            user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
            customer=Customer.objects.create(user=user,name=username,email=email,reff_code=result)
            user.save();
            customer.save();

            login(request,user,backend='django.contrib.auth.backends.ModelBackend')

            booking_rooms=request.COOKIES['booking-details'] 
            booking_rooms = list(eval(booking_rooms))
            hotelid = 0

            for booking_room in booking_rooms:

                print(booking_room)
                hotel=Hoteladmin.objects.get(id=int(booking_room['hotelid']))
                hotelid = hotel.id
                room=Rooms.objects.get(id=int(booking_room['roomid']))
                print('date',booking_room['checkin'])
                checkindates=booking_room['checkin'].split("-")
                checkin=checkindates[2]+"-"+checkindates[0]+"-"+checkindates[1]
                checkoutdates=booking_room['checkout'].split("-")
                checkout=checkoutdates[2]+"-"+checkoutdates[0]+"-"+checkoutdates[1]


                booking,created=Booking.objects.get_or_create(customer=customer,hotel=hotel,complete=False)
                booking.total_price=int(booking_room['totalprice'])
                booking.check_in=checkin
                booking.check_out=checkout
                booking.total_guest=booking_room['totalguest']
                roombooked,created=Roombooked.objects.get_or_create(booking=booking,room=room)
                roombooked.quantity=int(booking_room['roomscount'])
                booking.save()
                roombooked.save()

            return redirect( 'booking',id=hotel.id)
