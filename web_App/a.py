import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import sqlite3
from sklearn.decomposition import PCA


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

coefficients = pd.DataFrame(data=model.coef_, index=X.columns, columns=['Coefficient'])

# Analyze the coefficients for the Room_name features
room_name_coefficients = coefficients.loc[['Room_name_Budget Room', 'Room_name_Standard Room', 'Room_name_Queen Room']]
print(room_name_coefficients)
# Print recommendations for room types based on coefficients
print("\nRecommendations for room types to increase rental prices:")

for name in ['I-ONES', 'Cozy Cabin', 'Ivy Cottage', 'Blue Heaven']:
    room_type = room_name_coefficients.idxmax()[0].split('_')[-1]
    print(f"For {name}: It should have more \"{room_type} Rooms\"")