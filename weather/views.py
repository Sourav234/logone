from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):

    cities = City.objects.all()    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=1c22e024f8be9d603889ecfd3454cef8'
    
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate


    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html',context) #returns the index.html template