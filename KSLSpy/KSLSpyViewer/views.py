from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect 
# Create your views here.

def login(request):
    return render(request, 'KSLSpyViewer/login.html')

def validateLogin(request):
    request.POST['email']
    return HttpResponseRedirect(reverse('KSLSpyViewer:index'))

def index(request):
    return render(request, 'KSLSpyViewer/index.html', {'postData': 123})