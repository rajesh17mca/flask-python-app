from flask import Blueprint, jsonify, request, current_app
from .services.weather_service import fetch_weather
from .services.currency_service import get_exchange_rate
from .services.coordinates_service import search_city_by_name
from .utils.json_logger import setup_logger
from flask import current_app

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/v1/list_api', methods=['GET'])
def get_api_data():
    current_app.logger.info("API List Executed successfully")
    return {
        'weather_api': '/api/v1/weather?city=<cityname>',
        'currency_api': '/api/v1/currency?base=<base>&target=<target>',
        'coordinates_api': '/api/v1/coordinates?place=<name_of_place>'
    }

@main_bp.route('/api/v1/weather', methods=['GET'])
def get_weather_data():
    city = request.args.get('city', default='', type=str)
    current_app.logger.info(f"Weather fetch initiated for the city {city}")
    resp = fetch_weather(city=city)
    current_app.logger.info(f"Weather fetch complete for the city is {resp}")
    return resp

@main_bp.route('/api/v1/currency', methods=['GET'])
def get_currency_data():
    base = request.args.get('base', default='USD', type=str)
    target = request.args.get('target', default='INR', type=str)
    current_app.logger.info(f"Currency exchange from {base} to {target}")
    resp = get_exchange_rate(base_currency=base, target_currency=target)
    current_app.logger.info(f"Currency exchange from {base} to {target} is {resp}")
    return resp

@main_bp.route('/api/v1/coordinates', methods=['GET'])
def get_coordinates_data():
    place = request.args.get('place', default='', type=str)
    current_app.logger.info(f"Location coordinates fetching for {place}")
    resp = search_city_by_name(place=place)
    current_app.logger.info(f"Location coordinates for {place} is {resp}")
    return resp