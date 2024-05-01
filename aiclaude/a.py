import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os




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
    features = ['length_of_stay', 'Name_Blue Heaven', 'Name_Ivy Cottage', 'Name_Cozy Cabin', 'Name_I-ONES',
                'Room_name_Budget Room', 'Room_name_Standard Room', 'Room_name_Queen Room',
                'Location_Ooty', 'Location_Coorg', 'Location_Fort Kochi', 'Location_Trivandrum']

    X = bookings_data[features]
    y = bookings_data['Rent']

    # Split the Data into Training and Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Machine Learning Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Calculate the overall percentage increase in rental prices for I-ONES homestay
    #X_ones = X_test[X_test['Name_I-ONES'] == 1]
    #y_ones_orig = model.predict(X_ones)

    if request.method == 'POST':
        selected_homestay = request.POST.get('selected_homestay')
        duration_increase = request.POST.get('duration_increase')
        if selected_homestay and duration_increase:
            duration_increase = float(duration_increase) / 100 + 1  # Convert to a factor
            X_ones = X_test[X_test[f'Name_{selected_homestay}'] == 1]
            y_ones_orig = model.predict(X_ones)
            X_ones_new = X_ones.copy()
            X_ones_new['length_of_stay'] *= duration_increase
            y_ones_new = model.predict(X_ones_new)
            overall_increase_percent = (y_ones_new.mean() - y_ones_orig.mean()) / y_ones_orig.mean() * 100

            context = {
                'overall_increase_percent': overall_increase_percent,
                'duration_increase': float(request.POST.get('duration_increase')),
                'selected_homestay': selected_homestay
            }
        else:
            context = {}
    else:
        context = {}

       
        return render(request, 'data.html', context)