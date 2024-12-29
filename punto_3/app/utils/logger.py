import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name (str): Name of the logger, typically the module name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f"{log_dir}/{name}_{today}.log")
    file_handler.setFormatter(formatter)
    
    # Add handler if it doesn't exist
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger
