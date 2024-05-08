import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
import tensorflow as tf
import matplotlib.pyplot as plt
import plotly.graph_objs as go


# Set seed value for random number generators
np.random.seed(0)
tf.random.set_seed(0)



dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, 'web_App_home_book2.csv')

df = pd.read_csv(file_path,index_col='Check_in',parse_dates=True)
df.index.freq='MS'

len(df)

train = df.iloc[:]
#test = df.iloc[36:]

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

scaler.fit(train)
scaled_train = scaler.transform(train)
#scaled_test = scaler.transform(test)


# define generator
n_input = 12
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)



# define model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# fit model
model.fit(generator,epochs=50)

test_predictions = []

first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))



for i in range(12):

    # get the prediction value for the first batch
    current_pred = model.predict(current_batch)[0]

    # append the prediction into the array
    test_predictions.append(current_pred)

    # use the prediction to update the batch and remove the first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)


true_predictions = scaler.inverse_transform(test_predictions)
print(true_predictions)




while(True):
    m=int(input("enter the month: "))
    if m==0:
        break
        
    print("the predicted sales for the the month",m,"is",true_predictions[m-1])
    # Get the index for the same month of the previous year
    prev_year_month = f"2023-{m:02d}"
    
    # Extract the rent for the month of the previous year
    rent_prev_year = df.loc[prev_year_month, 'Rent'].values[0]

    print("\nThe previous year sales for the month",m,"is",rent_prev_year)



# Plotting the interactive graph using Plotly
actual_rent = go.Scatter(x=df.index[-12:], y=df['Rent'].values[-12:], mode='lines', name='Actual Rent')
predicted_rent = go.Scatter(x=df.index[-12:], y=true_predictions.flatten(), mode='lines', name='Predicted Rent')

layout = go.Layout(title='Actual vs Predicted Rent for 2023',
                   xaxis=dict(title='Month'),
                   yaxis=dict(title='Rent'))

fig = go.Figure(data=[actual_rent, predicted_rent], layout=layout)
fig.show()





