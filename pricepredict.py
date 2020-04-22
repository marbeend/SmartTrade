import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
from generate_dataset import get_data
import os

graph_count = 1
def predict(data, forecast_period=365, filename = 'prediction'):

    '''
    parameters:
     'data' should be AlphaVantage stock dataset
     'forecast_period' is the number of days forward to simulate
     'filename' is name of graph for UI

    '''

    #Get dates and values (time series) from 'data' dataframe for Prophet 
    ts = data.rename(columns={'1. open': 'open',
                '2. high': 'high',
                '3. low': 'low',
                '4. close': 'y',
                '5. volume': 'volume',
                'date': 'ds'})[['ds','y']]

    #Capture current information for UI
    current_date = str(ts['ds'].values[0])[0:10]
    current_price = float(ts['y'].values[0])
    
    #Create Prophet model and fit it to given time series
    m = Prophet()
    m.fit(ts)
    
    #Simulate future
    future = m.make_future_dataframe(periods=forecast_period)
    forecast = m.predict(future)

    #Capture predicted information for UI
    predicted_price = float(forecast['yhat'].values[-1])
    forecast_date = str(forecast['ds'].values[-1])[0:10]

    #bypass Flask caching by changing graph filename with each request
    global graph_count
    graph_count += 1
    path_to_graph = f'./static/images/{graph_count}_{filename}.png'

    #if the graph exists remove it. --- eventually, display it instead
    if os.path.isfile(path_to_graph):
        os.remove(path_to_graph)

    #Create plot
    m.plot(forecast, figsize=(6, 3.5), xlabel="Date", ylabel=f"Price of {filename} stock ($)").savefig(path_to_graph)
    
    #Buy/Sell decision
    if predicted_price > current_price:
        decision = True
    else:
        decision = False

    return decision, path_to_graph, current_price, current_date, predicted_price, forecast_date
