from flask import Flask, g, request
from uuid import uuid4
import time
from .utils.json_logger import setup_logger
from .utils.logging_context import TransactionIdFilter

def create_app(config_class='app.config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logger = setup_logger(
        logger_name=app.name, 
        log_file=app.config.get('LOG_FILE', 'app.log')
    )
    logger.addFilter(TransactionIdFilter())

    app.logger = logger
    app.logger.info("Application factory initialized")

    @app.before_request
    def add_transaction_id():
        g.txn_id = request.headers.get("X-Transaction-Id", str(uuid4()))
        g.start_time = time.perf_counter()
        app.logger.info("request_started", extra={"event": "request_started"})

    @app.after_request
    def add_txn_id_to_response(response):
        g.time_taken_ms = round((time.perf_counter() - g.start_time) * 1000, 2)
        app.logger.info(
            "request_completed",
            extra={"event": "request_completed"}
        )
        response.headers["X-Transaction-Id"] = g.txn_id
        return response
    
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app