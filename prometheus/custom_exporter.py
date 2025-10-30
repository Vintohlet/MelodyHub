"""
Custom Weather Exporter for Kazakhstan using OpenWeather API
Collects weather metrics for multiple cities.
"""

from prometheus_client import start_http_server, Gauge
import requests
import time
import logging
import sys
import os
from dotenv import load_dotenv

# --- Load API key from .env ---
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    logging.error("OPENWEATHER_API_KEY not found in .env")
    sys.exit(1)

# --- Настройка логгирования ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- Список крупных городов Казахстана ---
cities = [
    {"name": "Astana", "lat": 51.1694, "lon": 71.4491},
    {"name": "Almaty", "lat": 43.2220, "lon": 76.8512},
    {"name": "Shymkent", "lat": 42.3417, "lon": 69.5901},
    {"name": "Karaganda", "lat": 49.8066, "lon": 73.0853},
    {"name": "Aktobe", "lat": 50.2839, "lon": 57.1668},
]

# --- Метрики ---
weather_temperature = Gauge('weather_temperature_celsius', 'Current temperature', ['city', 'country'])
weather_temperature_min = Gauge('weather_temperature_min_celsius', 'Minimum temperature', ['city', 'country'])
weather_temperature_max = Gauge('weather_temperature_max_celsius', 'Maximum temperature', ['city', 'country'])
weather_feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature', ['city', 'country'])  # 👈 добавлено
weather_windspeed = Gauge('weather_windspeed_kmh', 'Current wind speed', ['city', 'country'])
weather_humidity = Gauge('weather_humidity_percent', 'Current humidity', ['city', 'country'])
weather_pressure = Gauge('weather_pressure_hpa', 'Air pressure', ['city', 'country'])
weather_precipitation = Gauge('weather_precipitation_mm', 'Precipitation', ['city', 'country'])
weather_cloudcover = Gauge('weather_cloudcover_percent', 'Cloud coverage', ['city', 'country'])
weather_api_response_time = Gauge('weather_api_response_time_seconds', 'API response time in seconds')
weather_api_calls_total = Gauge('weather_api_calls_total', 'Total successful API calls')

# --- Функция получения данных ---
def fetch_weather_data():
    success_calls = 0
    for city in cities:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': city['lat'],
                'lon': city['lon'],
                'appid': API_KEY,
                'units': 'metric'
            }

            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            weather_api_response_time.set(response_time)

            response.raise_for_status()
            data = response.json()

            labels = {'city': city['name'], 'country': 'Kazakhstan'}

            weather_temperature.labels(**labels).set(data['main'].get('temp', 0))
            weather_temperature_min.labels(**labels).set(data['main'].get('temp_min', 0))
            weather_temperature_max.labels(**labels).set(data['main'].get('temp_max', 0))
            weather_feels_like.labels(**labels).set(data['main'].get('feels_like', 0))  
            weather_windspeed.labels(**labels).set(data.get('wind', {}).get('speed', 0))
            weather_humidity.labels(**labels).set(data['main'].get('humidity', 0))
            weather_pressure.labels(**labels).set(data['main'].get('pressure', 0))
            weather_precipitation.labels(**labels).set(data.get('rain', {}).get('1h', 0))
            weather_cloudcover.labels(**labels).set(data.get('clouds', {}).get('all', 0))

            logging.info(f"✅ Weather data updated for {city['name']}")
            success_calls += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"⚠️ Weather API request failed for {city['name']}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error for {city['name']}: {e}")

    weather_api_calls_total.set(success_calls)

# --- Запуск сервера ---
if __name__ == '__main__':
    start_http_server(8000)
    logging.info("Custom Prometheus Exporter started on port 8000")

    while True:
        try:
            fetch_weather_data()
        except KeyboardInterrupt:
            logging.info("Exporter stopped manually.")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        time.sleep(20)  # обновление каждые 20 секунд
