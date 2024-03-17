from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


def front_page(request):
    return render(request, "home.html")

def admin_page(request):
    return render(request, "admin.html")

def user_page(request):
    return render(request, "user.html")

def book_homestay(request):
    home_stay = Homestay_details.objects.all()
    print(home_stay)
    home_stays= {'home_stay': home_stay}
    return render(request, "homestay_booking.html",home_stays)

def book_bike(request):
    bike_station = Bikestation_details.objects.all()
    bike_stations= {'bike_station': bike_station}
    return render(request, "bike_booking.html",bike_stations)

def manage_page(request):
    result1 = Bike_detail.objects.all()
    result2 = Homestay_details.objects.all()
    results_ = {'result1': result1,'result2': result2}
    return render(request, "manage.html",results_)

def manage_booking(request):
    result1 = Bike_books.objects.all()
    result2 = Home_book.objects.all()
    results_ = {'result1': result1,'result2': result2}
    return render(request, "book_manage.html",results_)



def bike_page(request):
    bike_station = Bikestation_details.objects.all()
    bike_stations= {'bike_station_': bike_station}
    return render(request, "bike.html",bike_stations)

def prediction_page(request):
    bikes = Bike_detail.objects.all()
    bike= {'bike': bikes}
    return render(request, "prediction_page.html",bike)

def house_page(request):
     return render(request, "house.html")

def bikestation_page(request):
    return render(request, "bike_station.html")

def feedback_user(request):
    return render(request, "feed_back.html")

def feedback_send(request):
    username = request.session["user_name_"]
    feedback = request.POST.get("feedback")
    obj = Feedback(User_name=username, Feedback=feedback)
    obj.save()
    return HttpResponse("<script>window.location.href='/feedback_user/';alert('Feedback Send Successfully')</script>")

def feedback_admin(request):
    feedbacks = Feedback.objects.all()
    feedback= {'feedback': feedbacks}
    return render(request, "feedback_admin.html",feedback)

def userdetails_page(request):
    user = User_details.objects.all()
    user_ = {'user_': user}
    return render(request, "user_details.html",user_)

def retrun_page(request):
    username = request.session["user_name_"]
    rent_detail= Bike_books.objects.filter(User_name=username,Status="On Rent").values()
    rent_details= {'rent_detail': rent_detail}
    return render(request, "retrun_bike.html",rent_details)

@csrf_exempt
def register(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    ph_no = request.POST.get("ph_no")
    password = request.POST.get("password")
    obj_reg = User_details.objects.filter(Email=email)
    x = obj_reg.count()
    print(x)
    if x != 1:
        obj = User_details(Full_name=name, Email=email, Phone_number=ph_no, Password=password)
        obj.save()
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "error"})


@csrf_exempt
def login(request):
    global user_name
    user_name = request.POST.get("user_name")
    log_password = request.POST.get("log_password")
    obj_login = User_details.objects.filter(Email= user_name , Password=log_password)
    y = obj_login.count()
    print(user_name,log_password)
    if y == 1:
        user = User_details.objects.get(Email=user_name, Password=log_password)
        request.session["id"] = user.Sl_no
        request.session["user_name_"] = user.Email
        return JsonResponse({"message": "success"})
    elif y == 0 and user_name == "admin" and log_password == "admin":
        return JsonResponse({"message": "admin"})
    else:
        return JsonResponse({"message": "error"})
    
def adding_homestay(request):
    name = request.POST.get("propertyName")
    type = request.POST.get("propertyType")
    location = request.POST.get("propertyLocation")
    price = request.POST.get("propertyPrice")
    ph_no = request.POST.get("phnno")
    print(name,type,location,price,ph_no)
    obj = Homestay_details(House_name=name, House_type=type, House_location=location, House_price=price, House_Phone=ph_no)
    obj.save()
    file_path = 'Web_app/entities/House_location.dat'
    add_place(file_path, location)
    return HttpResponse("<script>window.location.href='/house_page/';alert('HomeStay added sucessfully')</script>")

def adding_bikes(request):
    station = request.POST.get("bikestation")
    name = request.POST.get("bikeName")
    type = request.POST.get("bikeType")
    price = request.POST.get("bikePrice")
    print(station,name,type,price)
    obj = Bike_detail(Bike_station=station, Bike_name=name, Bike_type=type, Bike_price=price)
    obj.save()
    return HttpResponse("<script>window.location.href='/bike_page/';alert('Bike added sucessfully')</script>")

def adding_bikestation(request):
    station_name = request.POST.get("stationName")
    long = request.POST.get("longitude")
    lat = request.POST.get("latitude")
    location = request.POST.get("stationLocation")
    print(station_name,long,lat,location)
    obj = Bikestation_details(Bikestation_name=station_name, latitude=float(long), longitude=float(lat), Bikestation_location=location)
    obj.save()
    return HttpResponse("<script>window.location.href='/bikestation_page/';alert('Station added sucessfully')</script>")

def edit_bike(request):
    sl_no = request.POST.get("sl_no")
    name = request.POST.get("name")
    station = request.POST.get("station")
    type = request.POST.get("type")
    price = request.POST.get("price")
    bike_edit = Bike_detail.objects.get(Sl_no=int(sl_no))
    bike_edit.Bike_name = name
    bike_edit.Bike_station = station
    bike_edit.Bike_type = type
    bike_edit.Bike_price = price
    bike_edit.save()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")


def delete_bike(request):
    sl_no = request.POST.get("hide")
    bike_delete = Bike_detail.objects.get(Sl_no=int(sl_no))
    bike_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def edit_homestay(request):
    sl_no = request.POST.get("sl_no")
    name = request.POST.get("name")
    type_ = request.POST.get("type")
    location = request.POST.get("location")
    price = request.POST.get("price")
    ph_no = request.POST.get("ph_no")
    hom_edit = Homestay_details.objects.get(Sl_no=int(sl_no))
    hom_edit.House_name = name
    hom_edit.House_type = type_
    hom_edit.House_location = location
    hom_edit.House_price = price
    hom_edit.House_Phone = ph_no
    hom_edit.save()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")


def delete_homestay(request):
    sl_no = request.POST.get("hide")
    fly_delete = Homestay_details.objects.get(Sl_no=int(sl_no))
    fly_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def bike(request):
    station_name = request.POST.get("name")
    print(station_name)
    bike_detail = list(Bike_detail.objects.filter(Bike_station=station_name,Bike_availability="Available").values())
    print(bike_detail)
    bike_details= {'bike_detail': bike_detail}
    return render(request, "bikes.html",bike_details)

def bike_payment(request):
    bike_name = request.POST.get("name")
    bike_station = request.POST.get("station")
    print(bike_name)
    bike_detail = Bike_detail.objects.get(Bike_name=bike_name,Bike_station=bike_station)
    bike_details= {'bike_detail': [bike_detail]}
    return render(request, "bike_rent.html",bike_details)

def bike_rent(request):
    bike_name = request.POST.get("name")
    username = request.session["user_name_"]
    bike_station = request.POST.get("station")
    print(bike_name)
    bike_detail = Bike_detail.objects.get(Bike_name=bike_name,Bike_station=bike_station)
    bike_status = Bike_detail.objects.get(Bike_name=bike_name,Bike_station=bike_station)
    bike_status.Bike_availability = "Rent"
    bike_status.save()
    station=bike_detail.Bike_station
    bikename = bike_detail.Bike_name
    rent = bike_detail.Bike_price
    rent_date = request.POST.get("selectDate")
    print(rent_date)
    obj = Bike_books(User_name=username,Bikestation_name=station, Bike_name=bikename, Bike_price=rent, Rent_date=rent_date)
    obj.save()
    return HttpResponse("<script>window.location.href='/user_page/';alert('Booking Sucessfull')</script>")
def add_to_table(bike_name,bike_station,rent_date):
    print(bike_name,str(bike_station),str(rent_date))
    bike_station = str(bike_station)
    rent_date = str(rent_date)
    print(type(bike_station))
    bike_station=bike_station[2:-2]
    rent_date = rent_date[2:-2]
    print(bike_station)
    print("***********")
    date_object = datetime.strptime(rent_date, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    bike_detail = Bike_detail.objects.get(Bike_name=bike_name,Bike_station=bike_station)
    bike_status = Bike_detail.objects.get(Bike_name=bike_name,Bike_station=bike_station)
    bike_status.Bike_availability = "Rent"
    bike_status.save()
    station=bike_detail.Bike_station
    bikename = bike_detail.Bike_name
    rent = bike_detail.Bike_price
    print(formatted_date)
    obj = Bike_books(User_name=user_name,Bikestation_name=station, Bike_name=bikename, Bike_price=rent, Rent_date=formatted_date)
    obj.save()

def return_bike(request):
    username = request.session["user_name_"]
    bike_name = request.POST.get("name")
    bike_station = request.POST.get("station")
    return_date = request.POST.get("selectDate")
    username = request.session["user_name_"]
    bike_detail = Bike_books.objects.get(Bikestation_name=bike_station, Bike_name=bike_name,User_name=username,Status="On Rent")
    print(bike_detail)
    rent_date = bike_detail.Rent_date
    
    rent = bike_detail.Bike_price
    print(rent_date)
    days = days_between_dates(str(rent_date),str(return_date))
    print(days)
    total_rent = int(rent)*int(days)
    print(total_rent)
    data = list(Bike_books.objects.filter(Bikestation_name=bike_station,Bike_name=bike_name,User_name=username,Status="On Rent").values())
    bike_ ={'bike_': data,"price":total_rent,"return":return_date}
    return render(request, "demo_payment.html",bike_)

def demo_payment(request):
    username = request.session["user_name_"]
    bike_name = request.POST.get("name")
    bike_station = request.POST.get("station")
    date = request.POST.get("date")
    rent_date=request.POST.get("rent_date")
    print(rent_date)
    price = request.POST.get("price")
    print(bike_station,bike_name,date,price)
    bike_detail = Bike_books.objects.get(Bikestation_name=bike_station, Bike_name=bike_name,User_name=username,Rent_date=rent_date,Status ="On Rent")
    bike_detail.total_amout = price
    bike_detail.Status = "Available"
    bike_detail.Return_date = date
    bike_detail.save()
    data = Bike_detail.objects.get(Bike_station=bike_station, Bike_name=bike_name)
    data.Bike_availability = "Available"
    data.save()
    return HttpResponse("<script>window.location.href='/user_page/';alert('Payment Sucessfull')</script>")

def select_homestay(request):
    home_stay = request.POST.get("name")
    home_stay_details = list(Homestay_details.objects.filter(House_name=home_stay).values())
    home_stays= {'home_stay': home_stay_details}
    return render(request, "home_stay_selection.html",home_stays)

def book_homestay_(request):
    home_stay = request.POST.get("name")
    checkin_day = request.POST.get("check_in_day")
    days = request.POST.get("num_nights")
    home_stay_details = list(Homestay_details.objects.filter(House_name=home_stay).values())
    home__ = Homestay_details.objects.get(House_name=home_stay)
    rent = home__.House_price
    total_rent = int(rent) * int(days)
    check_out = calculate_date_after_days(str(checkin_day),int(days))
    home_stays= {'home_stay': home_stay_details,'check_in':checkin_day,'check_out':check_out,'rent':total_rent}
    return render(request, "homestay_payment.html",home_stays)

def payment_homestay(request):
    username = request.session["user_name_"]
    home_stay = request.POST.get("name")
    checkin_day = request.POST.get("check_in_day")
    rent = request.POST.get("total_rent")
    checkout_day = request.POST.get("check_out_day")
    home_stay_ = Homestay_details.objects.get(House_name=home_stay)
    type = home_stay_.House_type
    location = home_stay_.House_location
    print(username,home_stay,location,checkin_day,checkout_day,rent,type)
    obj = Home_book(User_name=username,Name=home_stay, Location=location, Check_in=checkin_day, Ckeck_out=checkout_day,Rent=rent , Type=type)
    obj.save()
    return HttpResponse("<script>window.location.href='/user_page/';alert('Payment Sucessfull')</script>")

def book_homestay_bot(request):
    # Open the file in read mode
    with open('homestay_booking_info.txt', 'r') as file:
        # Read the line containing the details
        details = file.readline().strip()

    # Split the details line by commas
    details_list = details.split(',')

    # Extracting values and storing them in variables
    homestay_name = details_list[0].split(':')[1].strip()
    number_of_nights = int(details_list[1].split(':')[1].strip())
    check_in_date = details_list[2].split(':')[1].strip()
    date_object = datetime.strptime(check_in_date, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    # Displaying the values (optional)
    print("Homestay Name:", homestay_name)
    print("Number of Nights:", number_of_nights)
    print("Check-in Date:", formatted_date)

    home_stay_details = list(Homestay_details.objects.filter(House_name=homestay_name).values())
    home__ = Homestay_details.objects.get(House_name=homestay_name)
    rent = home__.House_price
    total_rent = int(rent) * int(number_of_nights)
    check_out = calculate_date_after_days(str(formatted_date),int(number_of_nights))
    home_stays= {'home_stay': home_stay_details,'check_in':formatted_date,'check_out':check_out,'rent':total_rent}
    return render(request, "homestay_payment.html",home_stays)



# views.py

import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from collections import Counter


def booking_analytics(request):
    spice_nm=[]
    spice_co=[]
    ##################################################################################################
   
    co1 = Home_book.objects.all().values()
    co1 = list(co1)
    names = [entry['Name'] for entry in co1]
    name_counts = Counter(names)
    unique_names = list(name_counts.keys())
    counts = list(name_counts.values())
    location = [entry['Location'] for entry in co1]
    location_counts = Counter(location)
    unique_location = list(location_counts.keys())
    count_location = list(location_counts.values())
    check_in = [entry['Check_in'] for entry in co1]
    print(check_in)
    months = [datetime.strptime(date, '%Y-%m-%d').strftime('%m') for date in check_in]
    check_in_counts = Counter(months)
    month_names = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }

    unique_check_in = [month_names[month] for month in check_in_counts.keys()]
    count_check_in = list(check_in_counts.values())

    print(unique_check_in) 
    print(count_check_in)
    type = [entry['Type'] for entry in co1]
    type_counts = Counter(type)
    unique_type = list(type_counts.keys())
    count_type = list(type_counts.values())
    check_in_ = [entry['Check_in'] for entry in co1]
    print(check_in)
    check_in_counts_ = Counter(check_in_)
    unique_check_in_ = list(check_in_counts_.keys())
    count_check_in_ = list(check_in_counts_.values())
    months = [datetime.strptime(date, '%Y-%m-%d').strftime('%m') for date in check_in]

# Define the sessions
    session_mapping = {
        '04': 'Session 1',  # April
        '05': 'Session 1',  # May
        '08': 'Session 2',  # August
        '09': 'Session 2',  # September
        '12': 'Session 3',  # December
        '01': 'Session 3'   # January
    }

    # Group months into sessions and count occurrences of each session
    session_counts = Counter(session_mapping.get(month, None) for month in months if month in session_mapping)

    # Get unique session names
    session_names = list(session_counts.keys())
    session_count = list(session_counts.values())
    # Output session names and counts
    print(session_names)
    print(session_count)
    ####################################################################################################
    return render(request, 'analytic.html',{'k1':unique_names,'k2':counts,'k3':unique_location,'k4':count_location,'k5':unique_check_in,'k6':count_check_in,'k7':unique_type,'k8':count_type,'k9':unique_check_in_,'k10':count_check_in_,'k11':session_names,'k12':session_count})

def bike_analytics(request):
   
    ##################################################################################################
   
    co1 = Bike_books.objects.all().values()
    co1 = list(co1)
    names = [entry['Bikestation_name'] for entry in co1]
    name_counts = Counter(names)
    unique_names = list(name_counts.keys())
    counts = list(name_counts.values())
    location = [entry['Bike_name'] for entry in co1]
    location_counts = Counter(location)
    unique_location = list(location_counts.keys())
    count_location = list(location_counts.values())
    check_in = [entry['Rent_date'] for entry in co1]
    print(check_in)
    months = [datetime.strptime(date, '%Y-%m-%d').strftime('%m') for date in check_in]
    check_in_counts = Counter(months)
    month_names = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }

    unique_check_in = [month_names[month] for month in check_in_counts.keys()]
    count_check_in = list(check_in_counts.values())

    print(unique_check_in) 
    print(count_check_in)
    type = [entry['Bike_price'] for entry in co1]
    type_counts = Counter(type)
    unique_type = list(type_counts.keys())
    count_type = list(type_counts.values())
    check_in_ = [entry['Rent_date'] for entry in co1]
    print(check_in)
    check_in_counts_ = Counter(check_in_)
    unique_check_in_ = list(check_in_counts_.keys())
    count_check_in_ = list(check_in_counts_.values())
    session_mapping = {
        '04': 'Session 1',  # April
        '05': 'Session 1',  # May
        '08': 'Session 2',  # August
        '09': 'Session 2',  # September
        '12': 'Session 3',  # December
        '01': 'Session 3'   # January
    }

    # Group months into sessions and count occurrences of each session
    session_counts = Counter(session_mapping.get(month, None) for month in months if month in session_mapping)

    # Get unique session names
    session_names = list(session_counts.keys())
    session_count = list(session_counts.values())
    # Output session names and counts
    print(session_names)
    print(session_count)
    ####################################################################################################
    return render(request, 'analytics_bike.html',{'k1':unique_names,'k2':counts,'k3':unique_location,'k4':count_location,'k5':unique_check_in,'k6':count_check_in,'k7':unique_type,'k8':count_type,'k9':unique_check_in_,'k10':count_check_in_,'k11':session_names,'k12':session_count})
   
def prediction(request):
    Station = request.POST.get("station")
    name = request.POST.get("name")
    price = request.POST.get("price")
    rent = request.POST.get("rent")
    print(Station,name,price,rent)
    obj_login = Bike_books.objects.filter(Bikestation_name= Station , Bike_name=name)
    y = obj_login.count()
    print(y)
    if y != 0 :
        p1 = int(y)*int(price)
        p2 = int(y)*int(rent)
        p3 = p1-p2
        # print(p3)
        if p3>0:
            return HttpResponse("<script>window.location.href='/prediction_page/';alert('You might receive an additional profit of Rs."+ str(p3) + ".')</script>")
        elif p3<0:
            return HttpResponse("<script>window.location.href='/prediction_page/';alert('You might incur an additional loss of  Rs."+ str(abs(p3)) + ".')</script>")
        else:
            return HttpResponse("<script>window.location.href='/prediction_page/';alert('No Increase In Price')</script>")
    else:
        return HttpResponse("<script>window.location.href='/prediction_page/';alert('There have been no bookings made for this bike yet.')</script>")

def days_between_dates(date_str1, date_str2):
    date_format = "%Y-%m-%d"
    
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)

    delta = date2 - date1

    num_of_days = delta.days

    return num_of_days


def calculate_date_after_days(start_date_str, num_of_days):
    date_format = "%Y-%m-%d"

    start_date = datetime.strptime(start_date_str, date_format)

    result_date = start_date + timedelta(days=num_of_days)

    return result_date.strftime(date_format)

def check_place_exists(file_path, place):
    try:
        with open(file_path, 'r') as file:
            places = file.read().splitlines()
            if place in places:
                return True
            else:
                return False
    except FileNotFoundError:
        print("File not found.")
        return False

def add_place(file_path, place):
    if not check_place_exists(file_path, place):
        with open(file_path, 'a') as file:
            file.write(place + '\n')
        print(f"Added {place} to {file_path}.")
    else:
        print(f"{place} already exists in {file_path}.")

from .homestaychat import Session_
from .bikechat import MySession
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache  # Importing never_cache decorator

session1 = Session_()
session2 = MySession()

@never_cache  # Adding never_cache decorator to prevent caching
def chatbot_interface(request):
    return render(request, 'chatbot_interface.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = session1.reply(user_input)
        if user_input=="exit":
            session1.reset_session()
            return JsonResponse({'response': "exit"})
        else:
        # If the response includes a DataFrame, convert it to HTML table
            dataframe_html = None
            if 'df' in response:
                dataframe = response['df']
                dataframe_html = dataframe.to_html()
        
            return JsonResponse({'response': response['text'], 'dataframe': dataframe_html})
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def get_response1(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = session2.reply(user_input)
        if user_input=="exit":
            session2.reset_session()
            return JsonResponse({'response': "exit"})
        else:
        # If the response includes a DataFrame, convert it to HTML table
            dataframe_html = None
            if 'df' in response:
                dataframe = response['df']
                dataframe_html = dataframe.to_html()
            
            return JsonResponse({'response': response['text'], 'dataframe': dataframe_html})
    return JsonResponse({'error': 'Invalid request'})