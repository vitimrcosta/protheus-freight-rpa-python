# ============================================================================
# src/logger_config.py
# Configuração centralizada de logging
# ============================================================================

import logging
from src.config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Evitar duplicação de handlers
    if logger.hasHandlers():
        return logger
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
