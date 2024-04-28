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
csv_file_path = os.path.join(dir_path, 'web_App_home_book1.csv')

# Load the data
bookings_data = pd.read_csv(csv_file_path)

# Convert check-in and check-out dates to datetime format
bookings_data['Check_in'] = pd.to_datetime(bookings_data['Check_in'], format='%d-%m-%Y')
bookings_data['Check_out'] = pd.to_datetime(bookings_data['Check_out'], format='%d-%m-%Y')

# Calculate the length of stay
bookings_data['length_of_stay'] = (bookings_data['Check_out'] - bookings_data['Check_in']).dt.days

# One-hot encode categorical variables
bookings_data = pd.get_dummies(bookings_data, columns=['Name', 'Room_name','Location'])


# Feature Selection
features = ['length_of_stay', 'Name_Blue Heaven', 'Name_Ivy Cottage', 'Name_Cozy Cabin', 'Name_I-ONES',
            'Room_name_Budget Room','Room_name_Standard Room','Room_name_Queen Room',
            'Location_Ooty', 'Location_Coorg', 'Location_Fort Kochi', 'Location_Trivandrum']

X = bookings_data[features]
y = bookings_data['Rent']

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
X_ones = X_test[X_test['Name_I-ONES'] == 1]
y_ones_orig = model.predict(X_ones)

X_ones_new = X_ones.copy()
X_ones_new['length_of_stay'] *= 1.2
y_ones_new = model.predict(X_ones_new)

overall_increase_percent = (y_ones_new.mean() - y_ones_orig.mean()) / y_ones_orig.mean() * 100

print(f"The rental prices for I-ONES will increase by {overall_increase_percent:.2f}% when the length of stay is increased by 20%.")

#which Room_name to increase rent

bookings_data['Booking_Date'] = bookings_data['Check_in'].dt.date

# Group the data by Booking_Date and Name to get the daily bookings for each homestay
daily_bookings = bookings_data.groupby(['Booking_Date', 'Name']).size().reset_index(name='Bookings')

for name, group in daily_bookings.groupby('Name'):
    plt.figure(figsize=(12, 6))
    group.set_index('Booking_Date')['Bookings'].plot(title=f'Daily Bookings for {name}')
    plt.xlabel('Date')
    plt.ylabel('Number of Bookings')
    plt.show()