import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import pandas

# Function that retrieves a stock symbol and puts it into variable "sym"
    #Get entry from form on dashboard.html and set it to stockSymbol

def retrieveStockSymbol(sym):
    stockSymbol = sym
    return stockSymbol

# Function that puts symbol get put into the AlphaVantage function

def plotData(avSymbol):
# Initalize access to AlphaVantage API
    ts = TimeSeries(key='insert alpha vantage key', output_format='pandas')
# Get Intraday data of stock symbol, with 1 minute interval, and set it to data
    data, metadata = ts.get_intraday(symbol=f"{avSymbol}",interval='1min', outputsize='full')
# with matplotlib, plot the data
    data['4. close'].plot()
# Set the title and save plotted data into png
    plt.title(f'Intraday Times Series for the {avSymbol} stock (1 min)')
    plt.savefig('static/images/plot.png')
