from alpha_vantage.timeseries import TimeSeries
import pandas

def get_data(symbol):
    ts = TimeSeries(key='8P9LU6XMCEXIQ5WU', output_format='pandas')
    data, meta_data = ts.get_daily(symbol, outputsize='full')
    path = f'./{symbol}_daily.csv'
    data.to_csv(path)
    return path

if __name__ == "__main__":
    generate_dataset('GOOGL')