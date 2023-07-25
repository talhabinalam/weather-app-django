import datetime
import requests
from django.shortcuts import render

def index(request):
    api_key = open('API_KEY', 'r').read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current, minutely, hourly, slerts&appid={}"
    
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)
        
        weather_data1, daily_forecasts1 = fetch_weather(city1, api_key, current_weather_url, forecast_url)
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None
            
            context = {
                'weather_data1': weather_data1,
                'daily_forecasts1': daily_forecasts1,
                'weather_data2': weather_data2,
                'daily_forecasts2': daily_forecasts2,
                
            }
            return render(request, 'app/index.html', context)
        
    else:
        return render(request, 'app/index.html')
    

def fetch_weather(city, api_key, current_weather_url, forecast_url):
    reponse = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = reponse['coord']['lat'], reponse['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    
    weather_data ={
        'city': city,
        'temperature': round(reponse['main']['temp']- 273.15, 2),
        'description': reponse['weather'][0]['description'],
        'icon': reponse['weather'][0]['icon']
    }
    
    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })
    
    return weather_data, daily_forecasts
