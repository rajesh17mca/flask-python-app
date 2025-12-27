import requests
from flask import current_app

def get_exchange_rate(base_currency, target_currency):
    api_key = current_app.config['CURRENCY_EXCHANGE_API_KEY']
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    current_app.logger.info(f"Making call to exchangerate API")
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return {'base_currency': base_currency, 'target_currency': target_currency, 'exchange_rate': data['conversion_rate']}
        else:
            current_app.logger.error("Fetching failed", exc_info={'error_code': response.status_code, 'error_details': response.text})
            return {'error_code': response.status_code ,'error_details': f"{data.get('error-type', 'Unknown error')}"}
    
    except Exception as e:
        current_app.logger.error("Exception occurred during making call", exc_info={'Error': f'An unexpected error occurred: {e}'})
        return {'Error': f'An unexpected error occurred: {e}'}

