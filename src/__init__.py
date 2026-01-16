# ============================================================================
# src/__init__.py
# Pacote principal do sistema RPA
# ============================================================================

__version__ = "1.0.0"
__author__ = "Sistema RPA de Automação de Pedidos"
__description__ = "Sistema de automação de processamento de pedidos com RPA"

from src.config import *
from src.logger_config import setup_logger

__all__ = ["setup_logger"]
