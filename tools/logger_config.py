import logging
from logging.handlers import RotatingFileHandler                # Local Dev Environment

def create_rotating_file_handler(filename, max_size=1e6, backup_count=10, encoding='utf-8', format=""):
    try:                                                        # Create a RotatingFileHandler with specified parameters
        handler = RotatingFileHandler(
            filename=filename,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding=encoding
        )
        handler.setLevel(logging.DEBUG)
        
        # Default formatter for GENERIC & DEBUG level
        datefmt = '%Y-%m-%d %H:%M:%S'
        if format == "":
            format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(format, datefmt)
        handler.setFormatter(formatter)

        return handler
    except Exception as e:
        print(f"Error creating rotating file handler: {e}")
        raise

def configure_logger(logger_type='logfile',filename=""):
                                                                # Configure the logger based on the specified type: logfile, warning or generic
    try:
        logger_type = logger_type.lower()                       # Convert logger_type to lowercase for case-insensitivity
        logger = logging.getLogger(logger_type)
        filename=filename.strip()
        
        if logger_type == 'logfile':
                                                                # for creation of event.log
            logger.setLevel(logging.DEBUG)
            if filename == "": filename = 'logfile.log'
            handler = create_rotating_file_handler(filename)

        elif logger_type == 'whatsapp':
                                                                # for creation of whatsapp log with wa_usage.json, trackable on monthly usage format
            logger.setLevel(logging.WARNING)
            if filename == "": filename = 'wa_usage.json'
            log_format = '{"log_datetime": "%(asctime)s", "mobile": "%(mobile)s", "category": "%(category)s", \
                "location": "%(location)s", "event_datetime": "%(event_datetime)s"}'
            handler = create_rotating_file_handler(filename, format=log_format)
        
        elif logger_type == 'generic':    
                                                                # for generic log, generally not used                        
            logging.basicConfig(level=logging.INFO)
            if filename == "": filename = 'generic.json'
            handler = create_rotating_file_handler(filename)
        
        else:
            raise ValueError(f"Invalid logger_type: {logger_type}")
        
        logger.addHandler(handler)
        return logger
    except Exception as e:
        print(f"Error configuring logger: {e}")
        raise



