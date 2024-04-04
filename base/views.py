from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #login is compulsory for any action
from django.http import HttpResponse
from django.contrib import messages
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm


def login_page(request):
    page = 'login_page'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,"User doesn't exit")
        user = authenticate(request,username= username,password = password)

        if user is not None: #if there is user in database
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or password does't exits")
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logout_page(request):
    logout(request) #it deletes the token
    return redirect('home')

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            #form.save(commit = False) it will return an object that hasn't yet been saved to the database
            user.username = user.username.lower()
            login(request,user) # it will automatically login user after registration
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    context = {
        'form':form
               }
    return render(request,'base/login_register.html',context)

def home(request):
    q =request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms':rooms,
        'topic':topics,
        'room_count':rooms_count
               }
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all() #model ko bhitra model ko sabai messages haru lai get garako

    context = {
        'rooms': room,
        'room_messages':room_message
        }
    return render(request,'base/room.html',context)

@login_required(login_url='login_page') 
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
       form = RoomForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('home')
            
    context = {'form': form}
    return render(request,'base/room_form.html',context)

@login_required(login_url= 'login_page')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form  = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not allowed to edit')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save() 
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url= 'login_page')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed to delete')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})