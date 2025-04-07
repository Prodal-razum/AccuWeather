import requests

# возвращает True, если погодные условия благоприятны, иначе False
def good_weather(weather_json):
    try:
        real_feel_temperature = float(weather_json["RealFeelTemperature"]["Value"])
        wind_speed = float(weather_json["Wind"]["Speed"]["Value"])
        rain_probability = float(weather_json["RainProbability"])
        visibility = float(weather_json["Visibility"]["Value"])
        uv_index = int(weather_json["UVIndex"])
        rain = float(weather_json["Rain"]["Value"])
        snow = float(weather_json["Snow"]["Value"])

        # Благоприятными считают погодные условия, при которых
        #
        # Температура от 0 до 35 градусов включительно
        # Скорость ветра не больше 50 км/ч
        # Вероятность дождя не больше 70%
        #
        # Ожидается дождь менее 20 мм рт. ст.
        # Ожидается снег менее 30 см(высота снежного покрова)
        # Видимость больше 1 км
        # УФ-индекс не больше 5

        if real_feel_temperature < 0  or real_feel_temperature > 35 or wind_speed > 50 or rain_probability > 70 \
            or rain >= 20 or snow >= 30 or visibility<=1 or uv_index > 5:
            return False
        return True

    except TypeError or ValueError:
        print("Данные были введены некорректно")
        return None

# Возвращает данные о погоде, которые будут показываться пользователю
def get_weather_summary(weather_json):
    real_feel_temperature = float(weather_json["RealFeelTemperature"]["Value"])
    wind_speed = float(weather_json["Wind"]["Speed"]["Value"])
    rain_probability = float(weather_json["RainProbability"])
    return {"temperature":real_feel_temperature,
            "wind": wind_speed,
            "rain_probability": rain_probability
            }

def get_weather_by_coords(lat, lon):
    # Читаем наш ключ из отдельного файла
    API_KEY = open("data/API_KEY.txt").read()

    # Делаем HTTP запрос к accuweather, чтобы узнать погоду на острове Мэн. В location будет лежать location key для нашего острова
    location = requests.get(f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={lat}%2C{lon}")

    # Если запрос был выполнен успешно, получаем погоду на острове
    if location.status_code == 200:
        json_location = location.json()
        location_key = json_location["Key"]
        result = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}?apikey={API_KEY}&details=true&metric=true")
        return result.json()[0]
    else:
        print(f"Неудачная попытка подключения к API, код ошибки: {location.status_code}")