import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
from generate_dataset import get_data
import os
import time
def predict(data, forecast_period=365, filename = 'prediction'):
    #Get dates and values (time series) from 'data' dataframe for Prophet 
    ts = data.rename(columns={'1. open': 'open',
                '2. high': 'high',
                '3. low': 'low',
                '4. close': 'y',
                '5. volume': 'volume',
                'date': 'ds'})[['ds','y']]
    
    #Create Prophet model and fit it to time series
    m = Prophet()
    m.fit(ts)
    
    #Simulate future
    future = m.make_future_dataframe(periods=forecast_period)
    forecast = m.predict(future)

    #forecast['yhat'][-forecast_period:].to_csv(f'{filename}_predictions.csv')

    path_to_graph = f'./static/images/{filename}.png'

    if os.path.isfile(path_to_graph):
    	os.remove(path_to_graph)
    	time.sleep(1)

    m.plot(forecast, figsize=(6, 3.5), xlabel="Date", ylabel=f"Price of {filename} stock ($)").savefig(path_to_graph)
    
    if forecast['yhat'].values[-1] > forecast['yhat'].values[-forecast_period]:
        decision = True
    else:
        decision = False
    
    return decision, path_to_graph
