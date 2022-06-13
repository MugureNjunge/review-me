from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from .forms import UserRegisterForm, ProfileForm, NewProjectForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import ProfileSerializer, ProjectSerializer, RatingSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    projects=Project.objects.all()
    return render(request,'index.html',{'projects':projects})

def UserProfile(request,user_id):
        profile=Profile.objects.get(id=user_id)
        context = {'profile':profile}
        return render(request, 'profile.html', context)

def EditProfile(request):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('index')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'editprofile.html',{'form':form})        

#an api to handle the requests
@api_view(['GET','POST'])
def profile_list(request, format=None):
    #get all profiles
    if request.method =='GET':
        profiles = Profile.objects.all()
        #serialize them
        serializer = ProfileSerializer(profiles, many=True)
        #return json
        return Response(serializer.data)
    if request.method =='POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

def project_list(request):
    projects = Project.objects.all()
    #serialize them
    serializer = ProjectSerializer(projects, many=True)
    #return json
    return JsonResponse({'projects':serializer.data})

def rating_list(request):
    ratings = Rating.objects.all()
    #serialize them
    serializer = RatingSerializer(ratings, many=True)
    #return json
    return JsonResponse({'ratings':serializer.data})

def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            # Profile.get_or_create(user=request.user)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Account created for { username }!!')
            return redirect('index')

    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            messages.success(request,('You information is not valid'))
            return redirect('sign-in')

    else:
        return render(request,'sign-in.html')

def signout(request):  
    logout(request) 

    return redirect('sign-in')

def newproject(request):
    current_user = request.user
    profile =Profile.objects.get(username=current_user)
    if request.method =='POST':
        form = NewProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.username = current_user
            # project.avatar = profile.avatar
            # project.country = profile.country

            project.save()
    else:
        form = NewProjectForm()

    return render(request,'new-project.html',{"form":form})    
