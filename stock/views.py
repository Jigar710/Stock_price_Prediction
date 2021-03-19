import json

from django.shortcuts import render, HttpResponse, redirect
from datetime import *
from django.contrib import messages
from stock.models import Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import nsepy
import pandas as pd

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    return render(request, 'index.html')


def about(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    return render(request, 'about.html')


def contact(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        mobino = request.POST.get('mobino')
        address = request.POST.get('address')
        date = datetime.today()
        contact = Contact(name=name, age=age, email=email, mobino=mobino, address=address, date=date)
        contact.save()
        messages.success(request, 'Form is successfully submitted.')
    return render(request, 'contact.html')


def login2(request):
    print(request)
    if request.method == "POST":
        login_user = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        user = authenticate(username=login_user, password=login_password)
        if user is not None:
            print("login")
            login(request, user)
            return redirect('/index')
            # A backend authenticated the credentials
        else:
            messages.success(request, 'Invalid Username or Password')
            return render(request, 'login.html')
    # No backend authenticated the credentials
    return render(request, 'login.html')


def pre(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    if request.method == "POST":
        symbol_name = request.POST.get('symbol_name')
        duration = int(request.POST.get('dura'))
        print("symbol_name")
        print(duration)
        today = date.today()
        start = today + timedelta(-duration)
        stockData = nsepy.get_history(symbol=symbol_name, start=start, end=today)
        stockData = stockData.reset_index()
        stockData['Date'] = stockData['Date'].astype(str)
        stockData = stockData.reindex(index=stockData.index[::-1])
        json_records = stockData.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data,
                   'duration' : duration,
                   'sym_name':symbol_name,
                   'visible' : "visible"}
        return render(request, 'pre.html', context)
    context = {'visible': "invisible"}
    return render(request, 'pre.html',context)

def logout2(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        pass
    if request.method == "POST":
        reg_user = request.POST.get('reg_username')
        reg_email = request.POST.get('reg_email')
        reg_password = request.POST.get('reg_password')
        user = User.objects.create_user(reg_user, reg_email, reg_password)
        user.save()
        return redirect('/login')
    # No backend authenticated the credentials
    return render(request, 'register.html')
