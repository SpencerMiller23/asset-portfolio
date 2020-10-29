from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

# Create your views here.
def index(request):
    return render (request, "holdings/layout.html")

# Create your views here.
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
