from flask import g, request, has_request_context
import logging

class TransactionIdFilter(logging.Filter):
    """Populates txn_id, uri, and time_taken_ms for non-request logs."""
    def filter(self, record):
        if has_request_context():
            record.txn_id = getattr(g, "txn_id", None)
            record.uri = f"{request.method} {request.path}"
            record.time_taken_ms = getattr(g, "time_taken_ms", None)
        else:
            record.txn_id = "N/A"
            record.uri = None
            record.time_taken_ms = None
        return True

class RequestLoggerAdapter(logging.LoggerAdapter):
    """Automatically inject txn_id, uri, time_taken_ms into all request logs."""
    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        if has_request_context():
            extra.setdefault("txn_id", getattr(g, "txn_id", None))
            extra.setdefault("uri", f"{request.method} {request.path}")
            extra.setdefault("time_taken_ms", getattr(g, "time_taken_ms", None))
        else:
            extra.setdefault("txn_id", "N/A")
            extra.setdefault("uri", None)
            extra.setdefault("time_taken_ms", None)
        kwargs["extra"] = extra
        return msg, kwargs