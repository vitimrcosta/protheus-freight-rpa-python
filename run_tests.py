#!/usr/bin/env python
# ============================================================================
# run_tests.py
# Script para executar testes do sistema
# ============================================================================

"""Executa os testes de validação do sistema RPA."""

if __name__ == "__main__":
    from tests.teste_sistema import TestadorSistema
    import sys
    
    testador = TestadorSistema()
    exit_code = testador.executar_todos_testes()
    sys.exit(exit_code)
