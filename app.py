from flask import Flask, render_template, url_for, redirect, request
from avChart import plotData, retrieveStockSymbol

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard", methods = ['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route("/dashboard", methods = ['POST'])
def dashboardPost():
    #Retrieve symbol from html form
    symbol = request.form["sym"]

    #Set symbol from form into variable
    enteredSymbol = retrieveStockSymbol(symbol)

    #PLot data from Alpha Vantage
    plotData(enteredSymbol)
    return render_template('dashboard.html', sym=symbol)

@app.route("/chart", methods = ['GET'])
def chart():
    return render_template('chart.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)
