from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

import requests
import json

from .models import User, Position, Profile

# Create your views here.
def index(request):
    return render (request, "holdings/layout.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "holdings/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "holdings/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "holdings/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "holdings/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "holdings/register.html")

@login_required
def dashboard(request):
    response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY", params={"symbol": "AAPL", "apikey": "4JU2DZ6Q8876MFXK"})
    data = response.json()
    symbol = data["Meta Data"]["2. Symbol"]
    price = data["Time Series (Daily)"]["2020-10-28"]["4. close"]
    response = requests.get("https://www.alphavantage.co/query?function=OVERVIEW", params={"symbol": "AAPL", "apikey": "4JU2DZ6Q8876MFXK"})
    data = response.json()
    name = data["Name"]
    return render (request, "holdings/dashboard.html", {
        'symbol': symbol,
        'name': name,
        'price': price
    })
