from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta,date
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def front_page(request):
    return render(request, "home.html")

def admin_page(request):
    return render(request, "admin.html")

def user_page(request):
    return render(request, "user.html")

def data_page(request):
    context = {
        'your_data': 'This is some data you can pass to the template'
    }
    return render(request, 'data.html', context)

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
    result3 = Bikestation_details.objects.all()
    result4 = Room_details.objects.all()
    results_ = {'result1': result1,'result2': result2,"result3":result3,"result4":result4}
    return render(request, "manage.html",results_)

def manage_booking(request):
    result1 = Bike_books.objects.all()
    result2 = Home_book1.objects.all()
    results_ = {'result1': result1,'result2': result2}
    return render(request, "book_manage.html",results_)

def manage_booking_(request):
    username = request.session["user_name_"]
    result1 = Bike_books.objects.filter(User_name=username).order_by('-Sl_no')
    result2 = Home_book1.objects.filter(User_name=username).order_by('-Sl_no')
    today = date.today()    
    today_ = today.strftime('%Y-%m-%d')
    print(today_)
    results_ = {'result1': result1,'result2': result2,'today':today_}
    return render(request, "book_management.html",results_)


def bike_page(request):
    bike_station = Bikestation_details.objects.all()
    bike_stations= {'bike_station_': bike_station}
    return render(request, "bike.html",bike_stations)

def room_page(request):
    home_stay = Homestay_details.objects.all()
    home_stays= {'home_stay_': home_stay}
    return render(request, "room.html",home_stays)

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
    ph_no = request.POST.get("phnno")
    home_image = request.FILES.get("homeImage")  # Get the uploaded image file

    image_filename = home_image.name

    # Construct the file path within the bike_images folder
    image_path = os.path.join('homestay_images', image_filename)

    # Check if the image already exists in the bike_images folder
    if default_storage.exists(image_path):
        # Use the existing file path
        home_image_path = image_path
    else:
        # Save the new image file
        file_content = ContentFile(home_image.read())
        home_image_path = default_storage.save(image_path, file_content)
        home_image_path = home_image_path

    print(name, type, location,ph_no)
    obj = Homestay_details(
        House_name=name,
        House_type=type,
        House_location=location,
        House_Phone=ph_no,
        House_image=home_image_path  # Store the uploaded image file object
    )
    obj.save()
    file_path = 'Web_app/entities/House_location.dat'
    add_place(file_path, location)
    return HttpResponse("<script>window.location.href='/house_page/';alert('HomeStay added sucessfully')</script>")

def adding_bikes(request):
    station = request.POST.get("bikestation")
    name = request.POST.get("bikeName")
    type = request.POST.get("bikeType")
    price = request.POST.get("bikePrice")
    bike_image = request.FILES.get("bikeImage")

    image_filename = bike_image.name

    # Construct the file path within the bike_images folder
    image_path = os.path.join('bike_images', image_filename)

    # Check if the image already exists in the bike_images folder
    if default_storage.exists(image_path):
        # Use the existing file path
        bike_image_path = image_path
    else:
        # Save the new image file
        file_content = ContentFile(bike_image.read())
        bike_image_path = default_storage.save(image_path, file_content)
        bike_image_path = bike_image_path

    print(station, name, type, price)
    obj = Bike_detail(
        Bike_station=station,
        Bike_name=name,
        Bike_type=type,
        Bike_price=price,
        Bike_image=bike_image_path  # Store the existing or new image file path with correct path
    )
    obj.save()
    return HttpResponse("<script>window.location.href='/bike_page/';alert('Bike added sucessfully')</script>")

def adding_homes(request):
    homestay = request.POST.get("homestay")
    roomname = request.POST.get("roomname")
    roomtype = request.POST.get("roomType")
    price = request.POST.get("roomPrice")
    dicsription = request.POST.get("roomDescription")
    obj = Room_details(Home_stay=homestay, Room_name=roomname, Room_type=roomtype, Price=price, Discription= dicsription)
    obj.save()
    return HttpResponse("<script>window.location.href='/room_page/';alert('Rooms added sucessfully')</script>")


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

def edit_bikestation(request):
    sl_no = request.POST.get("sl_no")
    station = request.POST.get("station")
    old_station = request.POST.get("old")
    lat = request.POST.get("lat")
    log = request.POST.get("log")
    loc = request.POST.get("loc")
    bike_edit_ = Bikestation_details.objects.get(Sl_no=int(sl_no))
    bike_edit_.Bikestation_name = station
    bike_edit_.latitude = lat
    bike_edit_.longitude = log
    bike_edit_.Bikestation_location = loc
    bike_edit_.save()
    bikes_to_update = Bike_detail.objects.filter(Bike_station=old_station)
    for bike in bikes_to_update:
        bike.Bike_station = station
        bike.save()

    return HttpResponse("<script>window.location.href='/manage_page/'</script>")


def delete_bikestation(request):
    sl_no = request.POST.get("hide")
    bike_delete = Bikestation_details.objects.get(Sl_no=int(sl_no))
    bike_delete.delete()
    old_station = request.POST.get("old_")
    bikes_to_delete = Bike_detail.objects.filter(Bike_station=old_station)
    bikes_to_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def edit_homestay(request):
    sl_no = request.POST.get("sl_no")
    name = request.POST.get("name")
    type_ = request.POST.get("type")
    location = request.POST.get("location")
    ph_no = request.POST.get("ph_no")
    old = request.POST.get("old")
    hom_edit = Homestay_details.objects.get(Sl_no=int(sl_no))
    hom_edit.House_name = name
    hom_edit.House_type = type_
    hom_edit.House_location = location
    hom_edit.House_Phone = ph_no
    hom_edit.save()
    home_to_update = Room_details.objects.filter(Home_stay=old)
    for home in home_to_update:
        home.Home_stay = name
        home.save()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def cancel1(request):
    sl_no = request.POST.get("hide")
    fly_delete = Bike_books.objects.get(Sl_no=int(sl_no))
    fly_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_booking_/'</script>")
def cancel2(request):
    sl_no = request.POST.get("hide")
    fly_delete = Home_book1.objects.get(Sl_no=int(sl_no))
    fly_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_booking_/'</script>")

def delete_homestay(request):
    sl_no = request.POST.get("hide")
    fly_delete = Homestay_details.objects.get(Sl_no=int(sl_no))
    fly_delete.delete()
    name = request.POST.get("old_")
    home_to_delete = Room_details.objects.filter(Home_stay=name)
    home_to_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def edit_room(request):
    sl_no = request.POST.get("sl_no")
    room = request.POST.get("room")
    room_type = request.POST.get("type")
    price = request.POST.get("price")
    discription = request.POST.get("dis")
    room_edit = Room_details.objects.get(Sl_no=int(sl_no))
    room_edit.Room_name = room
    room_edit.Room_type = room_type
    room_edit.Price = price
    room_edit.Discription = discription
    room_edit.save()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")


def delete_room(request):
    sl_no = request.POST.get("hide")
    fly_delete = Room_details.objects.get(Sl_no=int(sl_no))
    fly_delete.delete()
    return HttpResponse("<script>window.location.href='/manage_page/'</script>")

def bike(request):
    station_name = request.POST.get("name")
    print(station_name)
    bike_detail = list(Bike_detail.objects.filter(Bike_station=station_name).values())
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
    rent_date = request.POST.get("selectDate")
    retun_date = request.POST.get("selectDate_")
    print(rent_date,retun_date)
    rent_date_ = datetime.strptime(rent_date, '%Y-%m-%d')
    return_date = datetime.strptime(retun_date, '%Y-%m-%d')
    rent_date_only = rent_date_.date()
    return_date_only = return_date.date()
    bookings = Bike_books.objects.filter(Bikestation_name=bike_station, Bike_name=bike_name)
    bike_detail = Bike_detail.objects.get(Bike_station=bike_station, Bike_name=bike_name)
    print(bike_detail)
    rent = bike_detail.Bike_price
    print(rent_date_only)
    print(return_date_only)
    days = days_between_dates(str(rent_date_only),str(return_date_only))
    print(days)
    total_rent = int(rent)*int(days)
    print(total_rent)
    data = list(Bike_detail.objects.filter(Bike_station=bike_station,Bike_name=bike_name).values())
    bike_ ={'bike_': data,"price":total_rent,"return":retun_date,'rent':rent_date}
    return render(request, "demo_payment.html",bike_)

def payment_bike(request):
    username = request.session["user_name_"]
    bike_name = request.POST.get("name")
    bike_station = request.POST.get("station")
    date = request.POST.get("date")
    rent_date=request.POST.get("rent_date")
    price = request.POST.get("price")
    bike_detail = Bike_detail.objects.get(Bike_station=bike_station, Bike_name=bike_name)
    print(bike_detail)
    rent = bike_detail.Bike_price
    obj = Bike_books(User_name=username, Bikestation_name=bike_station, Bike_name=bike_name, Rent_date=rent_date, Return_date=date,total_amout=int(price),Bike_price=int(rent))
    obj.save()
    return HttpResponse("<script>window.location.href='/user_page/';alert('Payment Sucessfull')</script>")

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
    data = list(Bike_detail.objects.filter(Bikestation_name=bike_station,Bike_name=bike_name).values())
    bike_ ={'bike_': data,"price":total_rent,"return":return_date}
    return render(request, "demo_payment.html",bike_)

def demo_payment(request):
    bike_name = request.POST.get("name")
    username = request.session["user_name_"]
    bike_station = request.POST.get("station")
    rent_date = request.POST.get("rent_date")
    retun_date = request.POST.get("date")
    rent = request.POST.get("price")
    
    data = list(Bike_detail.objects.filter(Bike_station=bike_station,Bike_name=bike_name).values())
    bike_ ={'bike_': data,"price":rent,"return":retun_date,'rent':rent_date}
    return render(request, "payment1.html",bike_)
    

def select_homestay(request):
    home_stay = request.POST.get("homestay")
    room_name = request.POST.get("room")
    home_stay_details = list(Room_details.objects.filter(Home_stay=home_stay,Room_name=room_name).values())
    home_stays= {'home_stay': home_stay_details}
    return render(request, "home_stay_selection.html",home_stays)

def select_room(request):
    home_stay = request.POST.get("name")
    home_stay_details = list(Room_details.objects.filter(Home_stay=home_stay).values())
    home_stays= {'home_stay': home_stay_details}
    return render(request, "room_selection.html",home_stays)

def book_homestay_(request):
    home_stay = request.POST.get("homestay")
    room_name = request.POST.get("room")
    checkin_day = request.POST.get("check_in_day")
    days = request.POST.get("num_nights")
    

    home_stay_details = list(Room_details.objects.filter(Home_stay=home_stay,Room_name=room_name).values())
    home__ = Room_details.objects.get(Home_stay=home_stay,Room_name=room_name)
    rent = home__.Price
    total_rent = int(rent) * int(days)
    check_out = calculate_date_after_days(str(checkin_day),int(days))
    rent_date = datetime.strptime(checkin_day, '%Y-%m-%d')
    return_date = datetime.strptime(check_out, '%Y-%m-%d')
        
    bookings = Home_book1.objects.filter(Name=home_stay)

    home_stays= {'home_stay': home_stay_details,'check_in':checkin_day,'check_out':check_out,'rent':total_rent}
    return render(request, "homestay_payment.html",home_stays)

def book_homestay__(request):
    home_stay = request.POST.get("homestay")
    room_name = request.POST.get("room")
    checkin_day = request.POST.get("checkin")
    checkout = request.POST.get("checkout")
    home_stay_details = list(Room_details.objects.filter(Home_stay=home_stay,Room_name=room_name).values())
    home__ = Room_details.objects.get(Home_stay=home_stay,Room_name=room_name)
    rent = home__.Price
    days = days_between_dates(str(checkin_day),str(checkout))
    total_rent = int(rent) * int(days)
    home_stays= {'home_stay': home_stay_details,'check_in':checkin_day,'check_out':checkout,'rent':total_rent}
    return render(request, "homestay_payment.html",home_stays)

def pay_page(request):
    home_stay = request.POST.get("homestay")
    room_name = request.POST.get("room")
    checkin_day = request.POST.get("check_in_day")
    rent = request.POST.get("total_rent")
    checkout_day = request.POST.get("check_out_day")
    home_stay_details = list(Room_details.objects.filter(Home_stay=home_stay,Room_name=room_name).values())
    home_stays= {'home_stay': home_stay_details,'check_in':checkin_day,'check_out':checkout_day,'rent':rent}
    return render(request, "payment_page.html",home_stays)

def payment_homestay(request):
    username = request.session["user_name_"]
    home_stay = request.POST.get("homestay")
    room_name = request.POST.get("room")
    checkin_day = request.POST.get("check_in_day")
    rent = request.POST.get("total_rent")
    checkout_day = request.POST.get("check_out_day")
    home_stay_ = Homestay_details.objects.get(House_name=home_stay)
    type = home_stay_.House_type
    location = home_stay_.House_location
    print(username,home_stay,location,checkin_day,checkout_day,rent,type)
    obj = Home_book1(User_name=username,Room_name=room_name,Name=home_stay, Location=location, Check_in=checkin_day, Check_out=checkout_day,Rent=rent , Type=type)
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

    home_stay_details = list(Room_details.objects.filter(Home_stay=homestay_name).values())
    home__ = Room_details.objects.filter(Home_stay=homestay_name)
    check_out = calculate_date_after_days(str(formatted_date),int(number_of_nights))
    home_stays= {'home_stay': home_stay_details,'check_in':formatted_date,'check_out':check_out}
    return render(request, "bot.html",home_stays)

def book_bike_bot(request):
    # Open the file in read mode
    with open('bike_booking_info.txt', 'r') as file:
        # Read the line containing the details
        details = file.readline().strip()

    details_list = details.split(',')

    bike_name = details_list[0].split(':')[1].strip()
    station = details_list[1].split(':')[1].strip()
    number_of_nights = int(details_list[2].split(':')[1].strip())
    check_in_date = details_list[3].split(':')[1].strip()
    date_object = datetime.strptime(check_in_date, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    print("bike Name:", bike_name)
    print("Number of Nights:", station)
    print("Check-in Date:", formatted_date)

    home_stay_details = list(Bike_detail.objects.filter(Bike_station=station,Bike_name=bike_name).values())
    home__ = Bike_detail.objects.get(Bike_station=station,Bike_name=bike_name)
    rent = home__.Bike_price
    total_rent = int(rent) * int(number_of_nights)
    check_out = calculate_date_after_days(str(formatted_date),int(number_of_nights))
    bike_ ={'bike_': home_stay_details,"price":total_rent,"return":check_out,'rent':formatted_date}
    return render(request, "demo_payment.html",bike_)

# views.py

import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from collections import Counter


def booking_analytics(request):
    spice_nm=[]
    spice_co=[]
    ##################################################################################################
   
    co1 = Home_book1.objects.all().values()
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
        '04': 'summer',  # April
        '05': 'summer',  # May
        '08': 'Onam',  # August
        '09': 'Onam',  # September
        '12': 'Christmas',  # December
        '01': 'Christmas'   # January
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
        '04': 'summer',  # April
        '05': 'summer',  # May
        '08': 'Onam',  # August
        '09': 'Onam',  # September
        '12': 'Christmas',  # December
        '01': 'Christmas'   # January
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
                print( response['text'])
            
            return JsonResponse({'response': response['text'], 'dataframe': dataframe_html})
    return JsonResponse({'error': 'Invalid request'})




# views.py
def data_page(request):
    # Get the directory path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # Construct the full file path
    conn = sqlite3.connect('db.sqlite3')
    # Query the table and load the data into a DataFrame
    query = "SELECT * FROM web_App_home_book1;"
    bookings_data = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    # Convert check-in and check-out dates to datetime format
    bookings_data['Check_in'] = pd.to_datetime(bookings_data['Check_in'], format='%Y-%m-%d')
    bookings_data['Check_out'] = pd.to_datetime(bookings_data['Check_out'], format='%Y-%m-%d')
    # Calculate the length of stay
    bookings_data['length_of_stay'] = (bookings_data['Check_out'] - bookings_data['Check_in']).dt.days
    # One-hot encode categorical variables
    bookings_data = pd.get_dummies(bookings_data, columns=['Name', 'Room_name', 'Location'])
    # Feature Selection
    features = ['length_of_stay', 'Name_Blue Heaven', 'Name_Ivy Cottage', 'Name_Cozy Cabin', 'Name_I-ONES', 'Room_name_Budget Room', 'Room_name_Standard Room', 'Room_name_Queen Room', 'Location_Ooty', 'Location_Coorg', 'Location_Fort Kochi', 'Location_Trivandrum']
    X = bookings_data[features]
    y = bookings_data['Rent']
    # Split the Data into Training and Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Train a Machine Learning Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    if request.method == 'POST':
        selected_homestay = request.POST.get('selected_homestay')
        duration_increase = request.POST.get('duration_increase')
        if selected_homestay and duration_increase:
            duration_increase = float(duration_increase) / 100 + 1
            X_ones = X_test[X_test[f'Name_{selected_homestay}'] == 1]
            y_ones_orig = model.predict(X_ones)
            X_ones_new = X_ones.copy()
            X_ones_new['length_of_stay'] *= duration_increase
            y_ones_new = model.predict(X_ones_new)
            overall_increase_percent = (y_ones_new.mean() - y_ones_orig.mean()) / y_ones_orig.mean() * 100
            y_ones_orig_mean = y_ones_orig.mean()
            y_ones_new_mean = y_ones_new.mean()
            amount_increase = y_ones_new_mean - y_ones_orig_mean

            # Assume the booking data represents bookings for one week
            weeks_in_year = 52
            amount_increase_yearly = amount_increase * weeks_in_year

            context = {
                'overall_increase_percent': overall_increase_percent,
                'duration_increase': float(request.POST.get('duration_increase')),
                'selected_homestay': selected_homestay,
                'amount_increase': amount_increase_yearly
            }
        else:
            context = {}
    else:
        context = {}

    return render(request, 'data.html', context)


# views.py
def data_bike(request):
    # Construct the full file path
    conn = sqlite3.connect('db.sqlite3')
    # Query the table and load the data into a DataFrame
    query = "SELECT * FROM web_App_bike_books;"
    bookings_data = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    # Convert check-in and check-out dates to datetime format
    bookings_data['Rent_date'] = pd.to_datetime(bookings_data['Rent_date'], format='%Y-%m-%d')
    bookings_data['Return_date'] = pd.to_datetime(bookings_data['Return_date'], format='%Y-%m-%d')
    # Calculate the length of stay
    bookings_data['length_of_stay'] = (bookings_data['Return_date'] - bookings_data['Rent_date']).dt.days
    # One-hot encode categorical variables
    bookings_data = pd.get_dummies(bookings_data, columns=['Bikestation_name', 'Bike_name'])
    # Feature Selection
    features = ['length_of_stay', 'Bikestation_name_Bikers Spots', 'Bikestation_name_Bikers Point', 'Bikestation_name_Bikers Hunt', 'Bikestation_name_Bikers Lover', 'Bikestation_name_Bikers Hub', 'Bikestation_name_iones two wheelers', 'Bike_name_Continental GT 650', 'Bike_name_Hunter 350', 'Bike_name_Himalayan 450', 'Bike_name_pulsar', 'Bike_name_DIO', 'Bike_name_Royal enfeild interceptor', 'Bike_name_Activa', 'Bike_name_Royal enfeild bullet 350']
    X = bookings_data[features]
    y = bookings_data['total_amout']
    # Split the Data into Training and Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Train a Machine Learning Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    if request.method == 'POST':
        selected_bikestation = request.POST.get('selected_bikestation')
        duration_increase = request.POST.get('duration_increase')
        if selected_bikestation and duration_increase:
            duration_increase = float(duration_increase) / 100 + 1
            X_ones = X_test[X_test[f'Bikestation_name_{selected_bikestation}'] == 1]
            y_ones_orig = model.predict(X_ones)
            X_ones_new = X_ones.copy()
            X_ones_new['length_of_stay'] *= duration_increase
            y_ones_new = model.predict(X_ones_new)
            overall_increase_percent = (y_ones_new.mean() - y_ones_orig.mean()) / y_ones_orig.mean() * 100
            y_ones_orig_mean = y_ones_orig.mean()
            y_ones_new_mean = y_ones_new.mean()
            amount_increase = y_ones_new_mean - y_ones_orig_mean

            # Assume the booking data represents bookings for one week
            weeks_in_year = 52
            amount_increase_yearly = amount_increase * weeks_in_year

            context = {
                'overall_increase_percent': overall_increase_percent,
                'duration_increase': float(request.POST.get('duration_increase')),
                'selected_bikestation': selected_bikestation,
                'amount_increase': amount_increase_yearly
            }
        else:
            context = {}
    else:
        context = {}

    return render(request, 'data_bike.html', context)





