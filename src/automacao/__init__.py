# ============================================================================
# src/automacao/__init__.py
# Módulos de automação e integração
# ============================================================================

from src.automacao.rpa_automacao import AutomacaoRPA, IntegracaoEmail
from src.automacao.integracao_email_real import IntegracaoEmailReal

__all__ = [
    "AutomacaoRPA",
    "IntegracaoEmail",
    "IntegracaoEmailReal",
]
