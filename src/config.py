# ============================================================================
# src/config.py
# Configurações centralizadas do projeto
# ============================================================================

import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"

# Criar diretórios se não existirem
for directory in [DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Arquivos
CSV_INPUT = DATA_DIR / "exemplo_pedidos.csv"
EXCEL_OUTPUT = OUTPUT_DIR / "relatorio_pedidos.xlsx"
PDF_OUTPUT = OUTPUT_DIR / "relatorio_pedidos.pdf"
LOG_FILE = LOGS_DIR / "aplicacao.log"

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de processamento
DIAS_ANTECEDENCIA_FRETE = 3  # Dias antes da data de embarque para agendar frete
DATA_FORMATO = "%d/%m/%Y"

# Configurações de RPA/Automação
EXECUTAR_AGENDADO = False  # Mudar para True para ativar execução agendada
INTERVALO_MINUTOS = 60  # Intervalo de execução agendada
