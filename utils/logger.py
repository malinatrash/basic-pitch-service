import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """Setup and return a configured logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if log_file is specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Create default logger
default_logger = setup_logger(
    'basic_pitch_service',
    os.path.join('logs', 'basic_pitch_service.log')
)
