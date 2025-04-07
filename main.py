from flask import Flask, render_template, request
from Weather import good_weather, get_weather_by_coords, get_weather_summary

app = Flask("AccuWeather")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из HTML-формы
        start_latitude = request.form.get('start-latitude')
        start_longitude = request.form.get('start-longitude')
        finish_latitude = request.form.get('finish-latitude')
        finish_longitude = request.form.get('finish-longitude')

        # Если все данные введены(проверка проводится "на всякий случай")
        # Есть еще одна проверка внутри самого HTML
        if (start_latitude and start_longitude and finish_latitude and finish_longitude):
            try:
                # пробуем конвертировать координаты в числа
                start_latitude = float(start_latitude)
                start_longitude = float(start_longitude)
                finish_latitude = float(finish_latitude)
                finish_longitude = float(finish_longitude)

                # Смотрим, попали ли координаты в допустимые значения
                # Данная проверка также необязательна
                if (-90 <= start_latitude <= 90 and -180 <= start_longitude <= 180 and
                    -90 <= finish_latitude <= 90 and -180 <= finish_longitude <= 180):

                    try:
                        # Получаем данные о погоде в этих точках
                        start_json = get_weather_by_coords(start_latitude, start_longitude)
                        finish_json = get_weather_by_coords(finish_latitude, finish_longitude)

                        # Проверяем начальную и конечную точку на погодные условия
                        if good_weather(start_json) and good_weather(finish_json):
                            return good(start_json, finish_json)
                        # Если условия неблагоприятные, сообщаем об этом пользователю
                        else:
                            return bad(start_json,finish_json)

                    # В случае ошибки выводим сообщение об ошибке
                    except TypeError:
                        return no_data()
                    except:
                        return error()

            except ValueError:
                return error()

    return render_template('index.html')

@app.route('/error/', methods = ["GET"])
def error():
    return render_template("error.html")

@app.route('/good/', methods = ["GET"])
def good(start_json, finish_json):
    # Получаем данные для вывода на экран
    start = get_weather_summary(start_json)
    finish = get_weather_summary(finish_json)

    start_temperature = start["temperature"]
    start_wind_speed = start["wind"]
    start_rain_probability = start["rain_probability"]

    finish_temperature = finish["temperature"]
    finish_wind_speed = finish["wind"]
    finish_rain_probability = finish["rain_probability"]

    return render_template("good.html",
                           start_temperature=start_temperature,
                           start_wind_speed=start_wind_speed,
                           start_rain_probability=start_rain_probability,
                           finish_temperature=finish_temperature,
                           finish_wind_speed=finish_wind_speed,
                           finish_rain_probability=finish_rain_probability)

@app.route('/bad/', methods = ["GET"])
def bad(start_json, finish_json):
    # Получаем данные для вывода на экран
    start = get_weather_summary(start_json)
    finish = get_weather_summary(finish_json)

    start_temperature = start["temperature"]
    start_wind_speed = start["wind"]
    start_rain_probability = start["rain_probability"]


    finish_temperature = finish["temperature"]
    finish_wind_speed = finish["wind"]
    finish_rain_probability = finish["rain_probability"]

    return render_template("bad.html",
                           start_temperature=start_temperature,
                           start_wind_speed=start_wind_speed,
                           start_rain_probability=start_rain_probability,
                           finish_temperature=finish_temperature,
                           finish_wind_speed=finish_wind_speed,
                           finish_rain_probability=finish_rain_probability)

@app.route('/no_data/', methods = ["GET"])
def no_data():
    return render_template("no_data.html")

if __name__ == "__main__":
    app.run(debug=True)