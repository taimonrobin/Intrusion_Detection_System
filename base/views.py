from django.db import models
from django.shortcuts import render
import mysql.connector
from unirostock.models import LogKzh
from .models import UniqueSourceAddr, SourceToDestination
from django.utils import timezone
from django_pandas.io import read_frame
from prophet.serialize import model_from_json
import json
import pandas as pd
import numpy as np
from .forms import UniqueSourceAddrForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def home(request):
    time_range = request.GET.get('time_range', '')
    # sql = "SELECT timestamp, source_addr, destination_addr FROM log_kzh WHERE timestamp >= NOW() - INTERVAL 1 MINUTE and apci != 'ACK' ORDER by timestamp"
    if time_range.count("1-day-data") > 0 or time_range.count("1-week-data") > 0 or time_range.count("1-month-data") > 0 or time_range.count("1-year-data") > 0:
        if time_range.count("1-day-data"):
            time_threshold = timezone.now() - timezone.timedelta(days=1)
        if time_range.count("1-week-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=7)   
        if time_range.count("1-month-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=30)   
        if time_range.count("1-year-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=365)   
    else:
        time_threshold = timezone.now() - timezone.timedelta(hours=1)   
    
    data = LogKzh.objects.filter(timestamp__gt=time_threshold).exclude(apci = 'ACK').using('uni_rostock_db')

    unique_source_addr = data.values_list('source_addr', flat=True)  

    unique_source_addr = set(unique_source_addr)

    address_list = []

    for i in unique_source_addr:

        x = {
            'address': i,
            'instant': data.filter(source_addr = i).count()
        }
        address_list.append(x)


    source_address_list = get_source_address_list()

    context = {'data':address_list,
                'from_time': time_threshold,
                'to_time': timezone.now(),
                'source_addresses': source_address_list
                }
    return render(request, 'base/home.html', context)

def source_address(request, address):
    tolerence_level = UniqueSourceAddr.objects.values_list('tolerence_level', flat=True).get(address=address)
    time_range = request.GET.get('time_range', 'None')
    time_threshold = timezone.now() - timezone.timedelta(hours=1)   

    if time_range.count("1-day-data") > 0 or time_range.count("1-week-data") > 0 or time_range.count("1-month-data") > 0 or time_range.count("1-year-data") > 0:
        if time_range.count("1-day-data"):
            time_threshold = timezone.now() - timezone.timedelta(days=1)
        if time_range.count("1-week-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=7)   
        if time_range.count("1-month-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=30)   
        if time_range.count("1-year-data") > 0:
            time_threshold = timezone.now() - timezone.timedelta(days=365)   
    data = LogKzh.objects.filter(timestamp__gt=time_threshold).exclude(apci = 'ACK').filter(source_addr=address).using('uni_rostock_db')

    counter = 1
    try:
        while(len(data) < 20):
            time_threshold = timezone.now() - timezone.timedelta(days=counter)
            data = LogKzh.objects.filter(timestamp__gt=time_threshold).exclude(apci = 'ACK').filter(source_addr=address).using('uni_rostock_db')
            counter = counter + 1 
            if(time_threshold.year < 2017):
                break
    except:
        data = LogKzh.objects.all().exclude(apci = 'ACK').filter(source_addr=address).using('uni_rostock_db')

    df = read_frame(data.values("source_addr", "timestamp")).set_index('timestamp')
    df["source_addr"] = 1
    df = df.resample("H").sum()
    df = df.reset_index()
    

    with open("static/prophet_model/"+address+".json", 'r') as fin:
        new_m = model_from_json(json.load(fin))  # Load model


    future = new_m.make_future_dataframe(periods=1000,freq='H',  include_history = True)
    forecast = new_m.predict(future)
    
    df["ds"] = df["timestamp"]
    df["y"] = df["source_addr"]
    results= pd.concat([df.set_index('ds')['y'],forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]],axis=1)
    results = results[time_threshold:timezone.now()]
    results['y'] = results['y'].fillna(0)
    results['yhat'] = results['yhat'].fillna(0)
    results['yhat_upper'] = results['yhat_upper'].fillna(0)
    results['yhat_lower'] = results['yhat_lower'].fillna(0)
    results.reset_index(inplace = True)
    results["ds"] = results["ds"].astype(str)


    print(new_m.plot_components(forecast))

    #Y
    y_df = results[["ds","y"]]
    list_of_y = []
    for index, value in enumerate(y_df.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_y.append(d)

    
    #Y hat
    yhat_df = results[["ds","yhat"]]
    list_of_yhat = []
    for index, value in enumerate(yhat_df.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_yhat.append(d)

    
    #Yhat upper
    yhat_upper_df = results[["ds","yhat_upper"]]
    list_of_yhat_upper = []
    for index, value in enumerate(yhat_upper_df.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_yhat_upper.append(d)


    #Yhat lower
    yhat_lower_df = results[["ds","yhat_lower"]]
    list_of_yhat_lower = []
    for index, value in enumerate(yhat_lower_df.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_yhat_lower.append(d)


    results['error'] = results['y'] - results['yhat']
    results["uncertainty"] = results['yhat_upper'] - results['yhat_lower']
    results[results['error'].abs() >  tolerence_level*results['uncertainty']]
    results['anomaly'] = results.apply(lambda x: 'Yes' if(np.abs(x['error']) >  tolerence_level*x['uncertainty']) else 'No', axis=1)
    
    #good_data
    good_data = results[(results["anomaly"] == "No")]
    good_data = good_data[['ds', 'y']]
    list_of_good_data = []
    for index, value in enumerate(good_data.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_good_data.append(d)

    #bad_data
    bad_data = results[(results["anomaly"] == "Yes")]
    bad_data = bad_data[['ds', 'y']]
    list_of_bad_data = []
    for index, value in enumerate(bad_data.values.tolist()):
        d = {
            'x': value[0],
            'y': value[1]
        }
        list_of_bad_data.append(d)


    #Boxplot
    list_of_boxplot = y_df["y"].values.tolist()

    #Histogram
    

    list_of_unique_y = list(set(list_of_boxplot))
    list_of_unique_y_instance = []
    for i in list_of_unique_y:
        list_of_unique_y_instance.append(list_of_boxplot.count(i))
    





    nav_bar = get_source_address_list()
    context = {'source_addresses': nav_bar, 'address': address, 'list_of_y': list_of_y,
     'list_of_yhat': list_of_yhat, 'list_of_yhat_upper': list_of_yhat_upper, 'list_of_yhat_lower': list_of_yhat_lower,
     'from_time': time_threshold, 'to_time': timezone.now(), 'list_of_good_data':list_of_good_data, 'list_of_bad_data':list_of_bad_data,
     'tolerence_level':tolerence_level, 'list_of_boxplot':list_of_boxplot, 'list_of_unique_y':list_of_unique_y, 'list_of_unique_y_instance':list_of_unique_y_instance}
    
    return render(request, 'base/source_address.html', context)

def change_tolerence_level(request, address):
    nav_bar = get_source_address_list()
    source_address = UniqueSourceAddr.objects.get(address = address)
    data = {'address': source_address.address, 'tolerence_level': source_address.tolerence_level}
    form = UniqueSourceAddrForm(data)
    if request.method == "POST":
        form = UniqueSourceAddrForm(request.POST)

        if form.is_valid():
            tolerence_level = form.cleaned_data['tolerence_level']
            UniqueSourceAddr.objects.filter(address = address).update(tolerence_level = tolerence_level)
            messages.success(request, 'Tolerence Level Successfully Saved')
    context = { 
        'form': form,
        'source_addresses': nav_bar,
        'address':address
    }

    return render(request, 'base/change_tolerence_level.html/', context)

def get_source_address_list():
    source_address_list = UniqueSourceAddr.objects.all()
    return source_address_list


