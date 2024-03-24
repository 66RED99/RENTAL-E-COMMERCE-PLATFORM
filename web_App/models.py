from django.db import models

# Create your models here.

class User_details(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    Full_name = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Phone_number = models.IntegerField()
    Password = models.CharField(max_length=255)

class Bike_detail(models.Model):
    Sl_no = models.IntegerField(primary_key=True) 
    Bike_station = models.CharField(max_length=255)
    Bike_name = models.CharField(max_length=255)
    Bike_type = models.CharField(max_length=255)
    Bike_price = models.IntegerField()
    Bike_availability = models.CharField(max_length=255,default="Available")
    Bike_image = models.ImageField(upload_to='bike_images/', blank=True, null=True)


class Homestay_details(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    House_name = models.CharField(max_length=255)
    House_type = models.CharField(max_length=255)
    House_location = models.CharField(max_length=255)
    House_price = models.IntegerField()
    House_Phone = models.IntegerField()
    House_image = models.ImageField(upload_to='homestay_images/', blank=True, null=True)

class Bikestation_details(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    Bikestation_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    Bikestation_location = models.CharField(max_length=255)

class Bike_books(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    User_name = models.CharField(max_length=255)
    Bikestation_name = models.CharField(max_length=255)
    Bike_name = models.CharField(max_length=255)
    Bike_price = models.IntegerField()
    Rent_date = models.CharField(max_length=255)
    Return_date = models.CharField(max_length=255,default="")
    Status = models.CharField(max_length=255,default="On Rent")
    total_amout = models.IntegerField(default=0)

class Home_book(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    User_name =  models.CharField(max_length=255)
    Name =  models.CharField(max_length=255)
    Location =  models.CharField(max_length=255)
    Check_in =  models.CharField(max_length=255)
    Ckeck_out =  models.CharField(max_length=255)
    Rent =  models.IntegerField()
    Type = models.CharField(max_length=255)

class Feedback(models.Model):
    Sl_no = models.IntegerField(primary_key=True)
    User_name =  models.CharField(max_length=255)
    Feedback =  models.CharField(max_length=255)

