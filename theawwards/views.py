from django.forms import GenericIPAddressField
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from .forms import UserRegisterForm, ProfileForm, NewProjectForm, RatingForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .serializers import ProfileSerializer, ProjectSerializer, RatingSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    projects=Project.objects.all()
    profile=Profile.objects.all()

    current_user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']

            rating = form.save(commit=False)

            rating.project = projects
            rating.profile = current_user
            rating.design = design
            rating.usability = usability
            rating.content = content
            rating.save()

        return redirect('index')

    else:
        form = RatingForm()

    return render(request,"index.html",{"projects":projects, "form": form,"profile":profile})
    
@login_required(login_url='/accounts/sign-in/')
def UserProfile(request):
    current_user = request.user
    user = current_user
    projects = Project.search_by_user(user)
    return render(request, 'profile.html',{'projects':projects})


def EditProfile(request):
    
    user = request.user.id
    current_user=request.user
    profile = Profile.objects.get(user_id=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.user = current_user
            profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.fullname = form.cleaned_data.get('fullname')
            profile.location = form.cleaned_data.get('location')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form':form,
    }
    return render(request, 'profile/edit.html', context)

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

@api_view(['GET','PUT','DELETE'])
def profile_detail(request,id, format=None):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    try:
        Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            

@api_view(['GET','POST'])
def project_list(request, format=None):
    #get all projects
    if request.method =='GET':
        project = Project.objects.all()
        #serialize them
        serializer = ProjectSerializer(project, many=True)
        #return json
        return Response(serializer.data)
    if request.method =='POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def project_detail(request,id, format=None):
    project = Project.objects.filter().first()
    try:
        Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            

def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
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

@login_required
def signout(request):  
    logout(request) 

    return redirect('sign-in')
          
@login_required(login_url='/accounts/sign-in/')
def NewProject(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('index')
        
    else:
        form = NewProjectForm()
    return render(request, 'new-project.html', {"form":form, "current_user":current_user})


def search(request):
    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_project = Project.search_by_projects(search_term)
        message = search_term

        return render(request,'search.html',{"message":message,
                                             "searched_project":searched_project})
    else:
        message = "You haven't searched for any project"
        return render(request,'search.html',{"message":message})        

@login_required(login_url='/accounts/sign-in/')
def add_rating(request, *args, **kwargs):
    pk = kwargs.get('pk')
    project = get_object_or_404(Project, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            review = form.save(commit=False)
            review.project = project
            review.user = current_user
            review.design = design
            review.usability = usability
            review.content = content
            review.save()
            return redirect('index')
    else:
        form = RatingForm()
        return render(request,'rating.html',{"user":current_user,"form":form})


