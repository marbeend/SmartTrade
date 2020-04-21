from flask import Flask, render_template, url_for, redirect, request
import datetime
import pricepredict
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/dashboard", methods = ['GET'])
def dashboard():
	return render_template('dashboard.html')


@app.route("/dashboard", methods = ['POST'])
def getStockData():
	#Retrieve symbol from html form
	symbol = request.form["sym"]

	#PLot data from Alpha Vantage
	#plotData(enteredSymbol)

	graph_path = None
	return render_template('dashboard.html', graph='./static/images/plot.png')
	# return redirect(url_for('chart'))
	# return render_template('dashboard.html', sym=symbol)
	# TODO: setup chart display 


@app.route("/pricepredict", methods = ['GET'])
def PricePredictHome():
	return render_template('pricepredict.html', graph=None)


@app.route("/pricepredict", methods = ['POST'])
def PricePredict():
	symbol = request.form["sym"].upper()
	try:
		forecast_period = int(request.form["forecast_period"])
	except:
		forecast_period = 365

	data_path = pricepredict.get_data(symbol)
	data = pd.read_csv(data_path)

	forecast_decision, path_to_graph = pricepredict.predict(data, forecast_period, symbol)

	if forecast_decision:
		decision = 'BUY!'
	else:
		decision = 'SELL!'

	return render_template('pricepredict.html', 
						   graph=path_to_graph,
						   decision=decision,
						   forecast_period = forecast_period,
						   symbol=symbol,)


if __name__ == "__main__":
	app.run(debug=True)