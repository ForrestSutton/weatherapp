import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time
import pytz


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://weather.db'


db = SQLAlchemy(app)

class City(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(50), nullable=False)
    zone   = db.Column(db.String(15), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    now = time.strftime('%l:%M %p %Z')
    utcnow = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    Edinburgh= utcnow.astimezone(pytz.timezone('Europe/London'))
    east = utcnow.astimezone(pytz.timezone('US/Eastern'))
    cent = utcnow.astimezone(pytz.timezone('US/Central'))
    west = utcnow.astimezone(pytz.timezone('US/Pacific'))

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=676a43c222cae620312f96afa8979df9'

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()

        weather = {
            'city' : city.name,
            'time' :  city.zone,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)
