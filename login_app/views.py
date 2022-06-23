from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
# Create your views here.
def index(request):
    return render(request,'login_registration.html')

def register(request):
    if request.method=='POST':
        errors=User.objects.basic_validation(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            user=User()
            user.first_name=request.POST.get('fname')
            user.last_name=request.POST.get('lname')
            user.email=request.POST.get('email')
            user.date=request.POST.get('date')
            user.pw=bcrypt.hashpw(request.POST.get('pw').encode(),bcrypt.gensalt()).decode()
            user.save()
            request.session['user_id']=user.id
            return redirect(reverse('success'))
    return redirect('/')

def login(request):
    if request.method=='POST':
        user=User.objects.filter(email=request.POST.get('email'))
        errors=User.objects.basic_validation(request.POST,user)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            request.session['user_id']=user[0].id
            return redirect(reverse('success'))
    return redirect('/')

def success(request):
    if 'user_id' in request.session:
        if request.method=='POST':
            if 'comment' in request.POST:
                comment=request.POST['comment']
                commment=Comment.objects.create(comment=comment,user_id=User.objects.get(id=request.session['user_id']),massage_id=Message.objects.get(id=request.POST['message1']))
                
            elif 'message' in request.POST:
                message=request.POST['message']
                Message.objects.create(message=message,user_id=User.objects.get(id=request.session['user_id']))
            return redirect(reverse('success'))
        context={
            'user':User.objects.get(id=request.session['user_id']),
            'messages_1':Message.objects.all().order_by('-created_at'),
            }
        return render(request, 'wall.html',context)
    return HttpResponse('Please login first')

def logout(request):
    try:
        for key in list(request.session.keys()):
            if not key.startswith("_"): # skip keys set by the django system
                del request.session[key]
    except KeyError:
        pass
    return redirect('/')

def delete(request):
    if request.method=='POST':
        if 'comment' in request.POST:
            comment_id=request.POST['comment']
            comment=Comment.objects.get(id=comment_id)
            difference= datetime.now() - comment.created_at
            duration_in_s = difference.total_seconds()  
            minutes = divmod(duration_in_s, 60)[0]  
            if minutes+1<30:
                comment.delete()
                messages.success(request, 'Comment was deleted successfully')
            else:
                messages.error(request, 'Comment time past 30 minuts')
        else:
            message_id=request.POST['message_delete']
            message=Message.objects.get(id=message_id)
            difference= datetime.now() - message.created_at
            duration_in_s = difference.total_seconds()  
            minutes = divmod(duration_in_s, 60)[0]  
            print('here')
            if minutes+1<30:
                message.delete()
                messages.success(request, 'Message was deleted successfully')
            else:
                messages.error(request, 'Comment time past 30 minuts')
            
        
    return redirect(reverse('success'))