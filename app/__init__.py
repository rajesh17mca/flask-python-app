from flask import Flask, g, request
from uuid import uuid4
import time
from .utils.json_logger import setup_logger
from .utils.logging_context import TransactionIdFilter, RequestLoggerAdapter

def create_app(config_class='app.config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup main logger
    logger = setup_logger(
        logger_name=app.name, 
        log_file=app.config.get('LOG_FILE', 'app.log')
    )
    logger.addFilter(TransactionIdFilter())
    app.logger = logger

    # Log app startup
    app.logger.info("Application factory initialized")

    # Helper to mask sensitive headers
    def sanitize_headers(headers):
        SENSITIVE = {"authorization", "cookie", "x-api-key"}
        return {k: ("***" if k.lower() in SENSITIVE else v) for k, v in headers.items()}

    @app.before_request
    def before_request_logging():
        g.txn_id = request.headers.get("X-Transaction-Id", str(uuid4()))
        g.start_time = time.perf_counter()
        g.logger = RequestLoggerAdapter(app.logger, {})  # wrap logger per request

        g.logger.info(
            "request_started",
            extra={
                "event": "request_started",
                "method": request.method,
                "extra_info": {
                    "request_headers": sanitize_headers(dict(request.headers)),
                    "query_params": request.args.to_dict(),
                    "remote_addr": request.remote_addr
                }
            }
        )

    @app.after_request
    def after_request_logging(response):
        log_level, message = define_log_event(response.status)
        g.time_taken_ms = round((time.perf_counter() - g.start_time) * 1000, 2)
        response.headers["X-Transaction-Id"] = g.txn_id
        getattr(g.logger, log_level)(
            message,
            extra={
                "event": "request_completed",
                "method": request.method,
                "extra_info": {
                    "response_headers": dict(response.headers),
                    "status_code": response.status_code
                }
            }
        )
        return response

    def define_log_event(status):
        if 100 <= status < 300:
            log_level = "info"
            message = "request_completed_success"
        elif 300 <= status < 400:
            log_level = "warning"
            message = "request_redirected"
        elif 400 <= status < 500:
            log_level = "error"
            message = "client_error"
        else:
            log_level = "critical"
            message = "server_error"
        return log_level, message
    
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app