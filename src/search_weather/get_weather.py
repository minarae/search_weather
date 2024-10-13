import requests
from datetime import datetime
from collections import defaultdict


class WeatherService:
    def __init__(self):
        self.api_key = None
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key

    def check_api_key(self):
        if not self.api_key:
            raise ValueError("API 키가 설정되지 않았습니다. 'set_api_key' 메서드를 사용하여 API 키를 설정해주세요.")

    def get_weather(self, latitude, longitude, target_date):
        try:
            self.check_api_key()
        except ValueError as e:
            return str(e)

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric",  # 섭씨 온도 사용
            "lang": "kr"  # 한국어로 결과 받기
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            daily_forecasts = defaultdict(lambda: {"temp_max": -float('inf'), "temp_min": float('inf'), "weather": []})

            for forecast in data['list']:
                forecast_date = datetime.fromtimestamp(forecast['dt']).date()
                if forecast_date == target_date:
                    daily_forecasts[forecast_date]["temp_max"] = max(daily_forecasts[forecast_date]["temp_max"], forecast['main']['temp_max'])
                    daily_forecasts[forecast_date]["temp_min"] = min(daily_forecasts[forecast_date]["temp_min"], forecast['main']['temp_min'])
                    daily_forecasts[forecast_date]["weather"].append(forecast['weather'][0]['description'])

            if target_date in daily_forecasts:
                forecast = daily_forecasts[target_date]
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


# WeatherService 인스턴스 생성
weather_service = WeatherService()
