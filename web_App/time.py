import pandas as pd
from fbprophet import Prophet

# Query the table and load the data into a DataFrame
query = "SELECT Check_in, Rent FROM web_App_home_book1;"
bookings_data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Convert check-in dates to datetime format
bookings_data['Check_in'] = pd.to_datetime(bookings_data['Check_in'], format='%Y-%m-%d')

# Prepare the time series data
bookings_ts = bookings_data.set_index('Check_in')['Rent'].resample('D').sum().reset_index()
bookings_ts.columns = ['ds', 'y']

# Initialize the Prophet model
model = Prophet()

# Fit the model on the historical data
model.fit(bookings_ts)

# Set the forecast period (e.g., 365 days for the next year)
future = model.make_future_dataframe(periods=365)

# Generate the forecasts
forecast = model.predict(future)

# Plot the forecasts
fig = model.plot(forecast)

# Extract the forecast values
forecast_values = forecast.loc[:, ['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(365)

# Print the forecast values
print(forecast_values) 