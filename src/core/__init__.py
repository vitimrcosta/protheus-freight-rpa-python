# ============================================================================
# src/core/__init__.py
# Módulos principais de processamento de dados
# ============================================================================

from src.core.leitor_csv import LeitorCSV
from src.core.processador_pedidos import ProcessadorPedidos
from src.core.gerador_relatorio import GeradorRelatorio

__all__ = [
    "LeitorCSV",
    "ProcessadorPedidos",
    "GeradorRelatorio",
]
