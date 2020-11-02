from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms

import requests
import json
import datetime
import time
import finnhub

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
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "holdings/register.html")

@login_required
def dashboard(request):
    return render (request, "holdings/dashboard.html")

def user_holdings(request):
    key = "buffvmn48v6o04cutb8g"
    finnhub_client = finnhub.Client(api_key=key)
    user = Profile.objects.get(user=request.user)
    positions = user.positions.all()
    data_response = {}
    data_response["holdings"] = []
    for position in positions:
        position_data = {}
        position_data["symbol"] = position.symbol
        try:
            data = finnhub_client.company_profile(symbol=position.symbol)
            name = data['name']
        except:
            name = "N/A"
        position_data["name"] = name
        try:
            data = finnhub_client.quote(position.symbol)
            price = data['c']
        except:
            price = "N/A"
        position_data["price"] = price
        data_response["holdings"].append(position_data)
    return JsonResponse(data_response, safe=False)

@csrf_exempt
def add_position(request):
    data = json.loads(request.body)
    symbol = data["symbol"]
    date = data["date"]
    shares = data["shares"]
    price = data["price"]
    position = Position.objects.create(symbol=symbol, date=date, shares=shares, price=price)
    position.save()
    profile = Profile.objects.get(user=request.user)
    profile.positions.add(position)
    profile.save()
    return JsonResponse({}, status=201)

def user_portfolio(request):
    key = "buffvmn48v6o04cutb8g"
    finnhub_client = finnhub.Client(api_key=key)
    user = Profile.objects.get(user=request.user)
    positions = user.positions.all()
    total_invested = 0
    total_value = 0
    data_response = {}
    for position in positions:
        initial_value = (position.shares) * (position.purchase_price)
        total_invested += initial_value
        data = finnhub_client.quote(position.symbol)
        price = data['c']
        total_value += int(price) * (position.shares)
    percent_change = ((total_value - total_invested) / total_invested) * 100
    data_response["value"] = round(total_value, 2)
    data_response["gains"] = round((total_value - total_invested), 2)
    data_response["change"] = round(percent_change, 2)
    return JsonResponse(data_response, safe=False)
