from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def login(request):
    return render(request,'auth/login.html')

@login_required
def home(request):
    return render(request,'auth/home.html')

def signup(request):
    return render(request,'auth/signup.html')       

# def logout(request):
#     # Perform any additional logout logic here
#     logout(request)
#     return redirect('login') 