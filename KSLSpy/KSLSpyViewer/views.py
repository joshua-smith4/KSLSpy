from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from KSLSpyViewer.models import *
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('KSLSpyViewer:dashboard'))
    return render(request, 'KSLSpyViewer/login.html')

def validateLogin(request):
    loginButtonClicked = False
    success = False
    try:
        request.POST['loginButton']
        loginButtonClicked = True
    except KeyError:
        pass
    email = request.POST['email']
    password = request.POST['password']
    if loginButtonClicked:
        u = authenticate(request, username=email, password=password)
        if u is not None and u.is_authenticated:
            login(request, u)
            success = True
        else:
            return render(request, 'KSLSpyViewer/login.html', {'errorMsg': 'Incorrect email or password'})
    else:
        try:
            newUser = User.objects.create_user(username=email, password=password, email=email)
            newUser.save()
            u = authenticate(request, username=email, password=password)
            if u is not None and u.is_authenticated:
                login(request,u)
            else:
                return render(request, 'KSLSpyViewer/login.html', {'errorMsg': 'Tried to authenticate but failed'})
        except:
            return render(request, 'KSLSpyViewer/login.html', {'errorMsg': 'User already exists'})
    return HttpResponseRedirect(reverse('KSLSpyViewer:dashboard'))

def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('KSLSpyViewer:login_view'))
    context = {
        'userData': request.user
    }
    print(request.user.campaign_set.all())
    return render(request, 'KSLSpyViewer/dashboard.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('KSLSpyViewer:login_view'))

def campaignNew(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('KSLSpyViewer:login_view'))
    return render(request, 'KSLSpyViewer/newCampaignForm.html')

def createNewCampaign(request):
    qJSON = {
        'keywords': request.POST['keywords'],
        'lower_price': request.POST['lower_price'],
        'higher_price': request.POST['higher_price'],
        'zipcode': request.POST['zipcode'],
        'distance_from_zip': request.POST['distance_from_zip'],
        'seller_type': request.POST['seller_type'],
        'listing_type': request.POST['listing_type'],
        'has_photos': request.POST['has_photos'],
        'time_since_posted': request.POST['time_since_posted'],
    }
    newCampaign = Campaign(user=request.user, queryJSON=json.dumps(qJSON), notify=True if request.POST['notify'] == 'on' else False)
    newCampaign.save()
    return HttpResponseRedirect(reverse('KSLSpyViewer:dashboard'))




