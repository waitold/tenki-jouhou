import requests
import json
import config
import kakasi
import collections

API_KEY = config.WEATHER_KEY
WEATHER = {"clear sky": "めっちゃ晴れ", "few clouds": "晴れ", "scattered clouds": "まぁ雲ある",
           "broken clouds": "それなりに曇ってる", "overcast clouds": "曇ってる", "shower rain": "避けれる雨",
           "rain": "まぁふつうの雨", "thunderstorm": "雷と雨", "snow": "雪ふってる", "mist": "霧かかってる"}


def get_current_weather(city_name):  # 地名を受け取り天候と最低、最高気温を返す
    api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city},JP&APPID={key}"
    url = api.format(city=city_name, key=API_KEY)
    res_data = requests.get(url)
    data = res_data.json()
    if data["cod"] == "404":
        return -1
    print(data["cod"])
    api_weather = data["weather"][0]["description"]
    temp_max = data["main"]["temp_max"]
    temp_min = data["main"]["temp_min"]
    return [WEATHER[api_weather], temp_max, temp_min]


def confirm_exists_city(city_name):
    api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city},JP&APPID={key}"
    url = api.format(city=city_name, key=API_KEY)
    res_data = requests.get(url)
    data = res_data.json()
    return data["cod"]


def get_days_forecast(city_name, days):  # 一日の天気予報を3時間ごとに返す（5日後まで可能）
    api = "http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city},JP&APPID={key}"
    url = api.format(city=city_name, key=API_KEY)
    res_data = requests.get(url)
    data = res_data.json()
    days_weather = []
    max_temp = []
    min_temp = []
    info = []

    for day in data["list"]:
        days_weather.append(day["weather"][0]["description"])
        max_temp.append(day["main"]["temp_max"])
        min_temp.append(day["main"]["temp_max"])
    info.append(days_weather[(days - 1)*8:days*8])
    info.append(max(max_temp))
    info.append(min(min_temp))
    return info


if __name__ == '__main__':
    print(kakasi.to_english("袖ヶ浦"))
    info = get_days_forecast("sodegaura", 1)
    get_current_weather("nagano")
    print(info)
