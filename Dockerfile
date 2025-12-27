FROM python:3.13-slim
WORKDIR /flask-app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--access-logfile", "/dev/null", "wsgi:app"]
