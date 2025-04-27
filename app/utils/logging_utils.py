import logging
import sys
from datetime import datetime
import os

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Set up logger with console and file handlers
    
    Args:
        name (str): Logger name
        log_file (str, optional): Path to log file
        level (int): Logging level
    
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_file():
    """Get default log file path based on current date"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    return os.path.join('logs', f'ats_{current_date}.log')

# Create default logger
default_logger = setup_logger(
    'smart_ats',
    log_file=get_default_log_file()
) 