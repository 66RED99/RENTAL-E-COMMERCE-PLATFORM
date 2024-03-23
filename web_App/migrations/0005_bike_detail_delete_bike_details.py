# Generated by Django 4.2.6 on 2024-03-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web_App", "0004_bikestation_details"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bike_detail",
            fields=[
                ("Sl_no", models.IntegerField(primary_key=True, serialize=False)),
                ("Bike_station", models.CharField(max_length=255)),
                ("Bike_name", models.CharField(max_length=255)),
                ("Bike_type", models.CharField(max_length=255)),
                ("Bike_price", models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name="Bike_details",
        ),
    ]