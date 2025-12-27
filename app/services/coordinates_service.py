import requests
from flask import current_app

def search_city_by_name(place):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={place}&count=1&language=en&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        
        if "results" in data:
            result = data['results'][0]
            return {
                "name": result['name'],
                "country": result['country'],
                "lat": result['latitude'],
                "lon": result['longitude']
            }
        
        else:
            current_app.logger.error("Fetching failed", exc_info={'error_code': response.status_code, 'error_details': response.text})
            return {'error_code': response.status_code, 'error_details': response.text}
    
    except Exception as e:
        current_app.logger.error("Exception occurred during making call", exc_info={'Error': f'An unexpected error occurred: {e}'})
        return {'Error': f'An unexpected error occurred: {e}'}