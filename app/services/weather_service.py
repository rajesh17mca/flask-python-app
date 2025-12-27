import requests
from flask import current_app

def fetch_weather(city):
    api_key = current_app.config['WEATHER_API_KEY']
    # params = { 'key': api_key, 'q': city, 'aqi': 'yes' }
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    current_app.logger.info(f"Running URL {url}", exc_info={'url': url})
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp_c = data['current']['temp_c']
            condition = data['current']['condition']['text']
            wind_kph = data['current']['wind_kph']
            return { 'condition': condition, 'weather': temp_c, 'wind': wind_kph }
        else:
            current_app.logger.error("Fetching failed", exc_info={'error_code': response.status_code, 'error_details': response.text})
            return {'error_code': response.status_code, 'error_details': response.text}
            
    except Exception as e:
        current_app.logger.error("Exception occurred during making call", exc_info={'Error': f'An unexpected error occurred: {e}'})
        return {'Error': f'An unexpected error occurred: {e}'}