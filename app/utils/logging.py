import logging
import logging.handlers
import sys

def setup_logger(logger_name='python_flask_app', log_file='app.log', console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False 

    console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760, # 10 MB
        backupCount=5
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

    # app_logger = setup_logger()