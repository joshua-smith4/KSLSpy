from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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
    return render(request, 'KSLSpyViewer/dashboard.html', {'userData':request.user.id})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('KSLSpyViewer:login_view'))








