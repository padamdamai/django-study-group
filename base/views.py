from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #login is compulsory for any action
from django.http import HttpResponse
from django.contrib import messages
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm


def login_page(request):
    page = 'login_page'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = email)
        except:
            messages.error(request,"User doesn't exit")
        user = authenticate(request,email= email,password = password)

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
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    rooms_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {
        'rooms':rooms,
        'topic':topics,
        'room_count':rooms_count,
        'room_message':room_messages
               }
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all().order_by('-created')
    #model ko bhitra model ko sabai messages haru lai get garako
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
        # create method is user to set,create and so on

    context = {
        'rooms': room,
        'room_messages':room_message,
        'participant':participants
        }
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topic = Topic.objects.all()
    context = {
        'user':user,
        'rooms':rooms,
        'room_message':room_message,
        'topic':topic
        
    }
    return render(request,'base/profile.html',context)


@login_required(login_url='login_page') 
def createRoom(request):
    form = RoomForm()
    topic = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
           host = request.user,
           topic = topic,
           name= request.POST.get('name'),
           description = request.POST.get('description'),

        )
        return redirect('home')
    
    context = {
        'form': form,
        'topic':topic
        }
    return render(request,'base/room_form.html',context)

@login_required(login_url= 'login_page')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form  = RoomForm(instance=room)
    topic = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed to edit')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.save()
        room.description = request.POST.get('description')


      
        return redirect('home')
    context = {
        'form':form,
        'topic':topic,
        'room':room
        }
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


@login_required(login_url= 'login_page')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed to delete')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url = 'login_page')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid:
            form.save()
            redirect('userProfile',pk= user.id)
    return render(request,'base/update-user.html',{'form':form})


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains = q)
    return render(request,'base/topics.html',{'topics':topic})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})