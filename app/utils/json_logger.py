import logging
import logging.handlers
import sys
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "event": getattr(record, "event", None),
            "txn_id": getattr(record, "txn_id", "N/A"),
            "uri": getattr(record, "uri", None),
            "time_taken_ms": getattr(record, "time_taken_ms", None),
            "message": record.getMessage(),
            "path": f"{record.pathname}:{record.lineno}",
            "func": record.funcName
        }

        if hasattr(record, 'extra_info'):
            log_record['extra'] = record.extra_info
            
        return json.dumps(log_record)

def setup_logger(logger_name='python_flask_app', log_file='app.log', console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False 

    json_formatter = JsonFormatter()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(json_formatter)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760, # 10 MB
        backupCount=5
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(json_formatter) # Set JSON here

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger