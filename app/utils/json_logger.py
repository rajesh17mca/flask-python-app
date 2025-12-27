import logging
import logging.handlers
import sys
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "event": getattr(record, "event", None),
            "txn_id": getattr(record, "txn_id", None),
            "uri": getattr(record, "uri", None),
            "time_taken_ms": getattr(record, "time_taken_ms", None),
            "message": record.getMessage(),
            "path": f"{record.pathname}:{record.lineno}",
            "func": record.funcName
        }

        # Include extra_info if present
        if hasattr(record, "extra_info") and record.extra_info:
            log_record["extra"] = record.extra_info

        # Remove None values
        log_record = {k: v for k, v in log_record.items() if v is not None}
        return json.dumps(log_record)

def setup_logger(logger_name='python_flask_app', log_file='app.log', console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = JsonFormatter()

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(console_level)
    ch.setFormatter(formatter)

    # File handler
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    fh.setLevel(file_level)
    fh.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
