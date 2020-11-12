from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
import requests
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
# Create your views here.




def home(request):
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
        otp=request.POST['otp']
        dicti = {"username":username,"email":email}
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
                user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
                user.save();

                login(request,user)

                return redirect(home)

            else:
               
                messages.info(request,'incorrect otp')
                return render(request,'user/user_login.html')
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



    

def hotel_view(request):
    return render(request,'user/hotel_view.html')

def booking(request):
    return render(request,'user/booking.html')


def hotel_list(request):
    return render (request,'user/hotel_listing.html')