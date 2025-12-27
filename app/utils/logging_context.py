from flask import g, request, has_request_context
import logging
import time

class TransactionIdFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.txn_id = getattr(g, "txn_id", "N/A")
            record.uri = f"{request.method} {request.path}"
            record.time_taken_ms = getattr(g, "time_taken_ms", None)
        else:
            record.txn_id = "N/A"
            record.uri = None
            record.time_taken_ms = None
        return True
