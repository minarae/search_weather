import requests
from datetime import datetime, timedelta
from collections import defaultdict


API_KEY = ""


def get_weather(latitude, longitude, target_date):
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

    # API 호출을 위한 매개변수 설정
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "date": target_date.date(),
        "units": "metric",  # 섭씨 온도 사용
        "lang": "kr"  # 한국어로 결과 받기
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        daily_forecasts = defaultdict(lambda: {"temp_max": -float('inf'), "temp_min": float('inf'), "weather": []})

        for forecast in data['list']:
            forecast_date = datetime.fromtimestamp(forecast['dt']).date()
            if forecast_date == target_date.date():
                daily_forecasts[forecast_date]["temp_max"] = max(daily_forecasts[forecast_date]["temp_max"], forecast['main']['temp_max'])
                daily_forecasts[forecast_date]["temp_min"] = min(daily_forecasts[forecast_date]["temp_min"], forecast['main']['temp_min'])
                daily_forecasts[forecast_date]["weather"].append(forecast['weather'][0]['description'])

        if target_date.date() in daily_forecasts:
            forecast = daily_forecasts[target_date.date()]
            most_common_weather = max(set(forecast["weather"]), key=forecast["weather"].count)

            return {
                "날짜": target_date.strftime("%Y-%m-%d"),
                "날씨": most_common_weather,
                "최고기온": f"{forecast['temp_max']:.1f}°C",
                "최저기온": f"{forecast['temp_min']:.1f}°C"
            }
        else:
            return "해당 날짜의 날씨 정보를 찾을 수 없습니다."
    else:
        return "날씨 정보를 가져오는데 실패했습니다."


# 사용 예시
if __name__ == "__main__":
    latitude = 37.5665  # 서울의 위도
    longitude = 126.9780  # 서울의 경도
    date = datetime.now() + timedelta(days=2)  # 모레의 날짜

    weather_info = get_weather(latitude, longitude, date)
    print(weather_info)
