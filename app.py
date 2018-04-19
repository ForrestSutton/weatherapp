import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=676a43c222cae620312f96afa8979df9'
    city = 'Las Vegas'
    r = requests.get(url.format(city)).json()
    print(r)
    
    weather = {
        'city': city,
        'tempature' : r['main']['temp'] ,
        'description': r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'], 
            
            
            }

    return render_template('weather.html')
