Step 1: Create the API Key for the currency exchange rates 
```
https://app.exchangerate-api.com/dashboard/confirmed
```

Step 2: Create the API key for the weather data
```
https://app.exchangerate-api.com/dashboard/confirmed
```

Step 3: We can use the following api for capturing the latitude and longitude of a given city
```
https://geocoding-api.open-meteo.com/v1/search?name=nellore&count=1&language=en&format=json
```

Create .env file
```
CURRENCY_EXCHANGE_API_KEY=<KEY Created in Step 1>
WEATHER_API_KEY=<KEY Created in Step 2>
```

#### Run as application
1. Close repository
2. cd flask-python-app
3. Create virtual env
```
python -m .venv venv
source .venv/bin/activate
```
4. run the following command to start the applicatioon
```
gunicorn wsgi:app
```
API's:
```
http://0.0.0.0:8080/api/v1/list_api
http://0.0.0.0:8080/api/v1/coordinates?place=<name_of_place>
http://0.0.0.0:8080/api/v1/currency?base=<base>&target=<target>
http://0.0.0.0:8080/api/v1/weather?city=<cityname>
```
Examples:
```
http://0.0.0.0:8080/api/v1/list_api
http://0.0.0.0:8080/api/v1/coordinates?place=nellore
http://0.0.0.0:8080/api/v1/currency?base=USD&target=INR
http://0.0.0.0:8080/api/v1/weather?city=nellore

#### Run as container
```
docker build -t flask-python-app .
docker run -d -p 80:8080 flask-python-app
docker ps
docker logs -f flask-python-app
```

API's:
```
http://0.0.0.0/api/v1/list_api
http://0.0.0.0/api/v1/coordinates?place=<name_of_place>
http://0.0.0.0/api/v1/currency?base=<base>&target=<target>
http://0.0.0.0/api/v1/weather?city=<cityname>
```
Examples:
```
http://0.0.0.0/api/v1/list_api
http://0.0.0.0/api/v1/coordinates?place=nellore
http://0.0.0.0/api/v1/currency?base=USD&target=INR
http://0.0.0.0/api/v1/weather?city=nellore
```
