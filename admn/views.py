from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import auth,User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from admn.models import Hoteladmin


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

    return render(request,'admin/admin_home.html')

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





