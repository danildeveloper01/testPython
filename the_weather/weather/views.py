import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=38765702a9209e4d4fa7814ec1e38113'

    
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            r = requests.get(url.format(new_city)).json()

            if r['cod'] == 200:
                form.save()
                message = 'City added successfully!'
                message_class = 'is-success'
            else:
                err_msg = 'City does not exist in the world!'
                message = err_msg
                message_class = 'is-danger'
           

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added  search!'
            message_class = 'is-success'


    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    

    for city in cities:

        r = requests.get(url.format(city)).json()

        if 'main' in r and 'weather' in r:
            city_weather = {
                'city_id': city.id,
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'windspeed' : r['wind']['speed'],
                'humidity' : r['main']['humidity'],
                'icon' : r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)



    weather_data.sort(key=lambda x: x['city_id'], reverse=True)
    context = {'weather_data' : weather_data, 
               'form' : form, 
               'message': message,
               'message_class': message_class}
    return render(request, 'weather/weather.html', context)


def delete_city_id(request, city_city_id):
    City.objects.get(id=city_city_id).delete()
    
    return redirect('home')














  