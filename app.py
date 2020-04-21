from flask import Flask, render_template, url_for, redirect, request
from avChart import plotData, retrieveStockSymbol
from flask import Flask , redirect , render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
import datetime

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
#app.config['SECRET_KEY']='b',h0\xa2\xa6\xa0\xd2\x1c8W\xb7\xe3\xd0\xdf\x9e\x8e\x90\xac9\x90\xc7\x81%\x8b''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200),unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    experience = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
@login_manager.user_loader
def get(id):
    return User.query.get(id)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard", methods = ['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route("/dashboard", methods = ['POST'])
def dashboardPost():
     if request.method == 'POST':
    #Retrieve symbol from html form
        symbol = request.form["sym"]
    #Set symbol from form into variable
        enteredSymbol = retrieveStockSymbol(symbol)
    #PLot data from Alpha Vantage
        plotData(enteredSymbol)
        return redirect(url_for('chart'))
        return render_template('dashboard.html', sym=symbol)

@app.route("/chart", methods = ['GET'])
def chart():
    return render_template('chart.html')
@app.route('/',methods=['GET'])
@login_required
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')



if __name__ == "__main__":
    app.run(debug=True)
