import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    city = 'Las Vegas'
    app_id = 'x'
    r = requests.get(url.format(city)(app_id)).json()
    print(r)

    weather = {
        'city': city,
        'tempature' : r['main']['temp'] ,
        'description': r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],


            }

    return render_template('weather.html')
