from django.shortcuts import redirect, render
import ccxt
import threading
from django.contrib import messages
import re
import sys
from numpy import number
import requests
from time import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from . import info
import datetime
from datetime import date, timedelta

from bs4 import BeautifulSoup

def home(request):
    return render(request, 'home.html')

#-------------------------------First Card(Price Check)---------------------------------------------#
def price(request):
    exchange = ccxt.gateio()
    markets = exchange.fetch_markets()

    if request.method =="POST":
        IP = request.POST['price']
        symbol = (f'{IP}/USDT')
        symbols = [symbol for symbol in [market['symbol'] for market in markets]]

        if symbol in symbols:
            messages.success(request," Entered  Coin is Availble")   
        else:
            messages.error(request, " Unfortunately, Entered  Coin is not listed")
            return redirect('price')
            
        def check():
            check.rate = exchange.fetch_ticker(symbol)['last']
            print(check.rate)

        def time(): 
            if symbol in symbols:
                threading.Timer(2, time).start()
                check()
        time()

        price.result=[]
        context ={
            'announ': check.rate,
            'coin': IP
        }
        price.result.append(context)
        print(check.rate)
        return redirect('price2')
    return render(request, 'price.html')
    

def price2(request):
    detail = price.result
    return render(request, 'price2.html', {'detail':detail})


#-------------------------------Second Card (Binance Announcement)----------------------------------------#

def listing(request):
    def List():
        la = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/catalog/list/query?catalogId=48&pageNo=1&pageSize=15")
        la = la.json()
        List.la = la['data']['articles'][0]['title']
        #List.la = ("Binance Will List Safemoon (ACA)")

        print(List.la)

        a = List.la.split()    
        b = ['Binance','Will','List']    
        c = a[:3]   

        if (c)==(b):
            List.f = (re.search(r'\(([^)]+)\)', List.la).group(1))
            print(List.f)
        else:
            List.f = "not match"
            print(List.f)

        
    def time():   
        threading.Timer(5.0, time).start()
        List()
    time()
    

    result=[]
    context ={
        'announ': List.la,
        'coin': List.f
    }
    result.append(context)
    return render(request, 'listing.html', {'result' : result})

#------------------------------- Recently added on coinmarketcap -----------------------------------------------#

def recent(request):

    # Get the html data with the help of parser and beautifulsoup
    url = "https://coinmarketcap.com/new/"
    data = requests.get(url)
    dta = BeautifulSoup(data.content, "html5lib")
    pretty_text = dta.prettify()
    #print(pretty_text)

    try:
        script = pretty_text.find("__NEXT_DATA__")
        data = pretty_text[script:script+500]

        coinindex = data.find("name")
        coin = data[coinindex+7:coinindex+20]

        result = ""
        for i in coin:
            if(i=='"'):
               break
            result = result + i
        #print(result)

        h1index = data.find("priceChange1h")
        h1 = data[h1index+15:h1index+20]
        #print(h1)

        h24index = data.find("priceChange24h")
        h24 = data[h24index+16:h24index+21]
        #print(h24)

        #print(f"new added coin is '{result}', 1 hour change:{h1}, 24 hour change:{h24}")

    except:
        new_pro1 = (f"Result not found plz contact develper")

    return render(request, 'recent.html', {'new_pro1' : result, "new_pro2": h1, "new_pro3": h24})
