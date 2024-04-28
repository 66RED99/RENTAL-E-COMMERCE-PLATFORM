import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
from pmdarima import auto_arima
import warnings

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full file path
csv_file_path = os.path.join(dir_path, 'web_App_home_book1.csv')

# Load the data
bookings_data = pd.read_csv(csv_file_path)

# Convert check-in and check-out dates to datetime format
bookings_data['Check_in'] = pd.to_datetime(bookings_data['Check_in'], format='%d-%m-%Y', errors='coerce')
bookings_data['Check_out'] = pd.to_datetime(bookings_data['Check_out'], format='%d-%m-%Y', errors='coerce')

# Calculate length of stay
bookings_data['length_of_stay'] = (bookings_data['Check_out'] - bookings_data['Check_in']).dt.days

bookings_data['Booking_Date'] = bookings_data['Check_in'].dt.date

# Drop rows with missing or invalid dates
bookings_data = bookings_data.dropna(subset=['Check_in', 'Check_out', 'length_of_stay'])

# Group the data by Name, Room_name, and length_of_stay to get the number of bookings for each combination
bookings_by_room_and_stay = bookings_data.groupby(['Name', 'Room_name', 'length_of_stay']).size().reset_index(name='Bookings')

# Get unique homestay names
homestay_names = bookings_by_room_and_stay['Name'].unique()

# Set the forecasting period (e.g., 30 days)
forecast_period = 30

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=Warning)

# Loop through each homestay
for homestay_name in homestay_names:
    # Get the room types for the current homestay
    room_types = bookings_by_room_and_stay[bookings_by_room_and_stay['Name'] == homestay_name]['Room_name'].unique()
    
    print(f"Homestay: {homestay_name}")
    
    for room_type in room_types:
        # Get the bookings for the current room type and homestay
        room_bookings = bookings_by_room_and_stay[(bookings_by_room_and_stay['Name'] == homestay_name) & (bookings_by_room_and_stay['Room_name'] == room_type)]
        
        # Fit an ARIMA model for each length of stay
        forecasts = []
        for length_of_stay, group in room_bookings.groupby('length_of_stay'):
            ts = group['Bookings']
            if len(ts.unique()) > 1:  # Check if the time series is not constant
                model = auto_arima(ts, start_p=0, start_q=0, seasonal=False, suppress_warnings=True)
                forecast = model.predict(n_periods=forecast_period)
                forecasts.append(forecast)
        
        # Combine the forecasts for all lengths of stay
        if forecasts:
            combined_forecast = pd.concat(forecasts, axis=1).mean(axis=1)
            avg_bookings = combined_forecast.mean()
        else:
            avg_bookings = 0
        
        # Get the current price for the current room type and homestay
        current_price = bookings_data[(bookings_data['Name'] == homestay_name) & (bookings_data['Room_name'] == room_type)]['Rent'].mean()
        
        # Adjust the price based on the average forecasted bookings
        if avg_bookings > 10:
            new_price = current_price * 1.2  # Increase price by 20% for high demand
        elif avg_bookings < 5:
            new_price = current_price * 0.8  # Decrease price by 20% for low demand
        else:
            new_price = current_price
        
        print(f"Forecasted average bookings for {homestay_name} - {room_type}: {avg_bookings:.2f}")
        print(f"Current price for {homestay_name} - {room_type}: {current_price:.2f}")
        print(f"Recommended new price for {homestay_name} - {room_type}: {new_price:.2f}")
        print()