from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import JsonResponse
from . import models
from django.contrib import messages
# Create your views here.
def home(request):
    API_KEY = '2a52a1ad16426d7457418f727afd018a'
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        city_name=request.POST.get('city')
        response = requests.get(url.format(city_name, API_KEY)).json()

        if response['cod'] == 200:
            if not models.City.objects.filter(name=city_name).exists():
                models.City.objects.create(name=city_name)
                messages.success(request, f'City {city_name} added successfully!')
            else:
                messages.warning(request, f'City {city_name} already exists!')
        else:
            messages.error(request, f'City {city_name} not found!') 
        return redirect('home')
    weather_data=[]
    try:
        cities=models.City.objects.all()
        for city in cities:
            response = requests.get(url.format(city.name, API_KEY)).json()
            if response['cod'] == 200:
                city_weather ={
                    'city': city.name,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon']
                }
                weather_data.append(city_weather)
            else:
                city.objects.filter(name=city.name).delete()
    except requests.RequestException:
        print ("Error fetching weather data")
    
    context={'weather_data': weather_data}
    return render(request, 'home.html', context)