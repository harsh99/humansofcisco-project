from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from .forms import UserSignupForm, CreateStoryForm
from django.contrib.auth.decorators import login_required
from .models import Story

def home(request):
    story= Story.objects.all().order_by('-created')
    return render(request, 'stories/home.html', {'stories': story})

#This method is for viewing the one clicked story specially when no user signed in
def readonlystories(request, story_pk):
    story= get_object_or_404(Story, pk=story_pk)
    story.refresh_from_db(fields=['viewcount'])
    Story.objects.filter(pk=story_pk).update(viewcount=F('viewcount')+1)
    form= CreateStoryForm(instance=story)
    if request.method == 'GET':
        return render(request, 'stories/readonlystories.html', {'story': story})

def signupuser(request):
    if request.user.is_authenticated:
        return redirect('readall')
    if request.method == 'GET':
        return render(request, 'stories/signupuser.html', {'form': UserSignupForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=request.POST['password1'])
                user.save()
                #login(request, user)--> Not logging in user directly, instead giving them link to login with account creation success
                messages.success(request, 'Account created successfully. Login to explore.')
                return redirect('signupuser')

            except IntegrityError:
                return render(request, 'stories/signupuser.html', {'form': UserSignupForm(), 'error':'Username exists, try another one.' })
        else:
            return render(request, 'stories/signupuser.html', {'form': UserSignupForm(), 'error':'Passwords didnt match, please try again' })

@login_required
def createstory(request):
    if request.method == 'GET':
        return render(request, 'stories/createstory.html', {'form': CreateStoryForm()})
    else:
        try:
            myform= CreateStoryForm(request.POST, request.FILES)
            if myform.is_valid():
                newStory= myform.save(commit=False)
                #return render(request, 'stories/createstory.html', {'form': CreateStoryForm(), 'newStory': newStory })
                newStory.user= request.user
                newStory.save()
                #messages.success(request, 'Congrats! Your Story joins the story pool...')
                return redirect('currentuser')
            else:
                return render(request, 'stories/createstory.html', {'form': CreateStoryForm(), 'error': 'Something went wrong with the submission, please submitted details try again!' })
        except ValueError:
            return render(request, 'stories/createstory.html', {'form': CreateStoryForm(), 'error': 'Invalid form data, please try again!' })

# This is to view a particular story
@login_required
def viewstory(request, story_pk):
    story= get_object_or_404(Story, pk=story_pk, user= request.user)
    form= CreateStoryForm(instance=story)
    if request.method == 'GET':
        return render(request, 'stories/viewstory.html', {'story': story, 'form':form})
    else:
        try:
            myform= CreateStoryForm(request.POST, instance=story)
            myform.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'stories/viewstory.html', {'story': story, 'form':form, 'error': 'Invalid Story entry, please try again.'})

@login_required
def deletestory(request, story_pk):
    story= get_object_or_404(Story, pk=story_pk, user= request.user)
    if request.method == 'POST':
        story.delete()
        return redirect('currentuser')

@login_required
def editstory(request, story_pk):
    story= get_object_or_404(Story, pk=story_pk, user= request.user)
    form= CreateStoryForm(instance=story)
    if request.method == 'GET':
        return render(request, 'stories/editstory.html', {'story': story, 'form':form})
    else:
        try:
            myform= CreateStoryForm(request.POST, request.FILES, instance=story)
            myform.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'stories/editstory.html', {'story': story, 'form':form, 'error': 'Invalid story entry, please try again.'})

@login_required
def currentuser(request):
    story= Story.objects.filter(user= request.user).order_by('-created')
    myStoryCount= story.count()
    totalViewCountForThisUser=0
    for s in story:
        totalViewCountForThisUser+= s.viewcount
    return render(request, 'stories/currentuser.html', {'stories': story, 'myStoryCount': myStoryCount, 'totalViewCountForThisUser':totalViewCountForThisUser})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('readall')
    if request.method == 'GET':
        return render(request, 'stories/loginuser.html', {'form': AuthenticationForm() })
    else:
        user= authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request, 'stories/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password didnt match, please try again' })
        else:
            login(request, user)
            return redirect('readall')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def aboutsite(request):
    if request.method == 'GET':
        return render(request, 'stories/aboutsite.html')
