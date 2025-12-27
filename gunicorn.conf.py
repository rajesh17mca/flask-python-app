bind = "0.0.0.0:8080"

workers = 2
threads = 4
worker_class = "gthread"

timeout = 120
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"