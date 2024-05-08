import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os



# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full file path
csv_file_path = os.path.join(dir_path, 'web_App_bike_books.csv')

# Load the data
bookings_data = pd.read_csv(csv_file_path)

# Convert check-in and check-out dates to datetime format
bookings_data['Rent_date'] = pd.to_datetime(bookings_data['Rent_date'], format='%Y-%m-%d')
bookings_data['Return_date'] = pd.to_datetime(bookings_data['Return_date'], format='%Y-%m-%d')

# Calculate the length of stay
bookings_data['length_of_stay'] = (bookings_data['Rent_date'] - bookings_data['Return_date']).dt.days

    # One-hot encode categorical variables
bookings_data = pd.get_dummies(bookings_data, columns=['Bikestation_name', 'Bike_name'])

    # Feature Selection
features = ['length_of_stay', 'Bikestation_name_Bikers Spots', 'Bikestation_name_Bikers Point', 'Bikestation_name_Bikers Hunt','Bikestation_name_Bikers Lover', 'Bikestation_name_Bikers Hub', 'Bikestation_name_iones two wheelers',
                'Bike_name_Continental GT 650', 'Bike_name_Hunter 350', 'Bike_name_Himalayan 450', 'Bike_name_pulsar', 'Bike_name_DIO', 'Bike_name_Royal enfeild interceptor', 'Bike_name_Activa', 'Bike_name_Royal enfeild bullet 350'
                ]

X = bookings_data[features]
y = bookings_data['total_amout']

    # Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Machine Learning Model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")



# Calculate the overall percentage increase in rental prices for I-ONES homestay
X_ones = X_test[X_test['Bikestation_name_Bikers Spots'] == 1]
y_ones_orig = model.predict(X_ones)

X_ones_new = X_ones.copy()
X_ones_new['length_of_stay'] *= 1.2
y_ones_new = model.predict(X_ones_new)

overall_increase_percent = (y_ones_new.mean() - y_ones_orig.mean()) / y_ones_orig.mean() * 100

print(f"The rental prices for I-ONES will increase by {overall_increase_percent:.2f}% when the length of stay is increased by 20%.")

