"""
URL configuration for bike_home_webapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web_App.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", front_page),
    path("front_page/", front_page, name="front_page"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("admin_page/", admin_page, name="admin_page"),
    path("userdetails_page/", userdetails_page, name="userdetails_page"),
    path("bike_page/", bike_page, name="bike_page"),
    path("house_page/", house_page, name="house_page"),
    path("bikestation_page/", bikestation_page, name="bikestation_page"),
    path("adding_bikestation/", adding_bikestation, name="adding_bikestation"),
    path("adding_bikes/", adding_bikes, name="adding_bikes"),
    path("adding_homestay/", adding_homestay, name="adding_homestay"),
    path("manage_page/", manage_page, name="manage_page"),
    path("edit_bike/", edit_bike, name="edit_bike"),
    path("delete_bike/", delete_bike, name="delete_bike"),
    path("edit_bikestation/", edit_bikestation, name="edit_bikestation"),
    path("delete_bikestation/", delete_bikestation, name="delete_bikestation"),
    path("edit_homestay/", edit_homestay, name="edit_homestay"),
    path("delete_homestay/", delete_homestay, name="delete_homestay"),
    path("edit_room/", edit_room, name="edit_room"),
    path("delete_room/", delete_room, name="delete_room"),
    path("data_page/", data_page, name="data_page"),
    path("data_bike/", data_bike, name="data_bike"),
    path("user_page/", user_page, name="user_page"),
    path("book_homestay/", book_homestay, name="book_homestay"),
    path("book_bike/", book_bike, name="book_bike"),
    path("bike/", bike, name="bike"),
    path("bike_payment/", bike_payment, name="bike_payment"),
    path("bike_rent/", bike_rent, name="bike_rent"),
    path("retrun_page/", retrun_page, name="retrun_page"),
    path("return_bike/", return_bike, name="return_bike"),
    path("demo_payment/", demo_payment, name="demo_payment"),
    path("select_homestay/", select_homestay, name="select_homestay"),
    path("book_homestay_/", book_homestay_, name="book_homestay_"),
    path("book_homestay__/", book_homestay__, name="book_homestay__"),
    path("payment_homestay/", payment_homestay, name="payment_homestay"),
    path("feedback_user/", feedback_user, name="feedback_user"),
    path("feedback_send/", feedback_send, name="feedback_send"),
    path("feedback_admin/", feedback_admin, name="feedback_admin"),
    path("booking_analytics/", booking_analytics, name="booking_analytics"),
    path("bike_analytics/", bike_analytics, name="bike_analytics"),
    path("prediction_page/", prediction_page, name="prediction_page"),
    path("prediction/", prediction, name="prediction"),
    path("chatbot_interface/", chatbot_interface, name="chatbot_interface"),
    path("get_response/", get_response, name="get_response"),
    path("get_response1/", get_response1, name="get_response1"),
    path("book_homestay_bot/", book_homestay_bot, name="book_homestay_bot"),
    path("manage_booking/", manage_booking, name="manage_booking"),
    path("book_bike_bot/", book_bike_bot, name="book_bike_bot"),
    path("manage_booking_/", manage_booking_, name="manage_booking_"),
    path("cancel1/", cancel1, name="cancel1"),
    path("cancel2/", cancel2, name="cancel2"),
    path("room_page/", room_page, name="room_page"),
    path("adding_homes/", adding_homes, name="adding_homes"),
    path("select_room/", select_room, name="select_room"),
    path("pay_page/", pay_page, name="pay_page"),
    path("payment_bike/", payment_bike, name="payment_bike")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)