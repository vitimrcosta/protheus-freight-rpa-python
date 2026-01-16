# Sistema RPA de Processamento de Pedidos

Sistema automatizado de processamento de pedidos com geração de relatórios em Excel, criação de fila de fretes e integração de email via RPA (Robotic Process Automation).

## 📋 Descrição

Este projeto automatiza o fluxo completo de processamento de pedidos:
- 📥 **Leitura de CSV**: Importa dados de pedidos de arquivo CSV
- 🔄 **Processamento**: Valida, transforma e agrega dados
- 📊 **Relatórios**: Gera relatórios em Excel com múltiplas abas
- 📅 **Fila de Fretes**: Cria agendamento automático de fretes
- 🤖 **Automação**: Executa tarefas em horários pré-definidos
- 📧 **Email**: Integração com sistemas de email para notificações

## ✨ Características Principais

- **Modular e Escalável**: Arquitetura baseada em pacotes Python profissional
- **Tratamento de Erros**: Sistema robusto de logging e tratamento de exceções
- **Testes Automatizados**: 7 testes cobrindo todas as funcionalidades (100% sucesso)
- **Documentação Completa**: Código bem comentado e documentação técnica
- **Agendamento**: Suporte a execução automática via scheduling
- **Cross-Platform**: Funciona em Windows, macOS e Linux

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

### Instalação

#### 1. Clonar o Repositório

```bash
# HTTPS
git clone https://github.com/vitimrcosta/protheus-freight-rpa-python.git
cd protheus-freight-rpa-python

# ou SSH (se configurado)
git clone git@github.com:vitimrcosta/protheus-freight-rpa-python.git
cd protheus-freight-rpa-python
```

#### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependências principais:**
- `pandas` - Processamento de dados
- `openpyxl` - Geração de arquivos Excel
- `schedule` - Agendamento de tarefas

## 📦 Estrutura do Projeto

```
rpa-processamento-pedidos/
│
├── src/                          # Código-fonte principal
│   ├── main.py                   # Orquestrador principal
│   ├── config.py                 # Configurações centralizadas
│   ├── logger_config.py          # Sistema de logging
│   │
│   ├── core/                     # Módulos de processamento
│   │   ├── leitor_csv.py         # Leitura e validação de CSV
│   │   ├── processador_pedidos.py # Transformação de dados
│   │   └── gerador_relatorio.py  # Geração de relatórios
│   │
│   └── automacao/                # Módulos de automação
│       ├── rpa_automacao.py      # Agendamento de tarefas
│       └── integracao_email_real.py # Integração de email
│
├── tests/                        # Testes e exemplos
│   ├── teste_sistema.py          # Suite de 7 testes
│   └── exemplo_uso_avancado.py   # 5 exemplos de uso
│
├── data/                         # Dados de entrada
│   └── exemplo_pedidos.csv       # Arquivo de exemplo
│
├── output/                       # Arquivos gerados
│   ├── relatorio_pedidos.xlsx    # Relatório em Excel
│   └── pedidos_customizado.csv   # Exportações customizadas
│
├── logs/                         # Arquivos de log
│   └── aplicacao.log             # Log de execução
│
├── docs/                         # Documentação
│   └── requirements.txt          # Dependências Python
│
├── main.py                       # Ponto de entrada
├── run_tests.py                  # Executor de testes
├── run_examples.py               # Executor de exemplos
├── setup.py                      # Configuração de pacote
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

## 🏃 Como Executar

### Execução Simples

Processa um arquivo CSV e gera relatório:

```bash
python main.py
```

**O que acontece:**
1. Lê `data/exemplo_pedidos.csv`
2. Valida e transforma os dados
3. Gera `output/relatorio_pedidos.xlsx`
4. Exibe relatório no console
5. Registra tudo em `logs/aplicacao.log`

### Executar Testes

Valida todas as funcionalidades:

```bash
python run_tests.py
```

**Saída esperada:**
```
✓ Teste 1: Verificar imports
✓ Teste 2: Verificar arquivos
✓ Teste 3: Leitura de CSV
✓ Teste 4: Processamento
✓ Teste 5: Geração de Relatório
✓ Teste 6: Automação
✓ Teste 7: Integração de Email

7/7 APROVADOS (100% SUCESSO)
```

### Executar Exemplos

Demonstra usos avançados do sistema:

```bash
python run_examples.py
```

**Exemplos incluídos:**
1. Processamento básico
2. Filtragem de fretes urgentes
3. Alertas customizados
4. Agendamento de tarefas
5. Exportação de dados

## 💻 Uso em Código

### Uso Básico

```python
from src.core import LeitorCSV, ProcessadorPedidos, GeradorRelatorio

# Ler dados
leitor = LeitorCSV()
dados = leitor.ler_dados()

# Processar
processador = ProcessadorPedidos()
totais_cliente = processador.calcular_total_por_cliente(dados)
fila_fretes = processador.criar_fila_fretes(dados)

# Gerar relatório
gerador = GeradorRelatorio()
gerador.gerar_excel(dados, totais_cliente, fila_fretes)
```

### Uso Avançado com Automação

```python
from src.automacao import AutomacaoRPA
from datetime import time

# Configurar automação
automacao = AutomacaoRPA()
automacao.agendar_tarefa(
    funcao=processar_pedidos,
    intervalo_minutos=30,
    horario_maximo=time(18, 0)
)

# Iniciar agendador
automacao.iniciar_scheduler()
```

### Importar Módulos Específicos

```python
from src.config import CSV_INPUT, DIAS_ANTECEDENCIA_FRETE
from src.logger_config import setup_logger

logger = setup_logger(__name__)
logger.info(f"Processando: {CSV_INPUT}")
```

## 🔧 Configuração

Edite `src/config.py` para customizar:

```python
# Caminhos
DATA_DIR = "data"
OUTPUT_DIR = "output"
LOGS_DIR = "logs"
CSV_INPUT = DATA_DIR / "exemplo_pedidos.csv"

# Frete
DIAS_ANTECEDENCIA_FRETE = 3  # Antecedência mínima

# Agendamento
EXECUTAR_AGENDADO = False  # True para modo scheduler
INTERVALO_MINUTOS = 30     # Intervalo entre execuções

# Email (se usar integracao_email_real.py)
EMAIL_REMETENTE = "seu-email@gmail.com"
EMAIL_DESTINATARIOS = ["destino@example.com"]
```

## 📊 Entrada e Saída

### Entrada (CSV)

Arquivo `data/exemplo_pedidos.csv` com colunas:
- `cliente` - Nome do cliente
- `produto` - Descrição do produto
- `quantidade` - Quantidade pedida
- `valor_unitario` - Valor por unidade
- `data_pedido` - Data do pedido (YYYY-MM-DD)

### Saída (Excel)

Arquivo `output/relatorio_pedidos.xlsx` com 3 abas:

1. **Resumo_Executivo**
   - Total de pedidos
   - Valor total
   - Quantidade total
   - Clientes atendidos

2. **Totais_Cliente**
   - Resumo por cliente
   - Quantidade e valor

3. **Fila_Fretes**
   - Fretes agendados
   - Datas e clientes

## 🧪 Testes

### Rodar Testes Específicos

```bash
python -m pytest tests/teste_sistema.py -v
```

### Cobertura de Testes

A suite `teste_sistema.py` valida:
- ✅ Importação de módulos
- ✅ Existência de arquivos
- ✅ Leitura de CSV
- ✅ Processamento de dados
- ✅ Geração de relatórios
- ✅ Automação e scheduling
- ✅ Integração de email

## 📚 Documentação Técnica

Para documentação técnica detalhada, veja [TECHNICAL.md](TECHNICAL.md)

Inclui:
- Arquitetura e design
- Explicação de cada módulo
- Fluxo de dados
- Tratamento de erros
- Exemplo de extensão

## 🐛 Troubleshooting

### Erro de Encoding no Windows

Se encontrar `UnicodeEncodeError`:

```bash
# Já configurado no src/main.py, mas se necesário:
set PYTHONIOENCODING=utf-8
python main.py
```

### Módulos não encontrados

Certifique-se de estar no diretório raiz:

```bash
cd rpa-processamento-pedidos
python main.py
```

### Arquivo CSV não encontrado

Verifique que `data/exemplo_pedidos.csv` existe com o formato correto.

## 📝 Log de Execução

Todos os eventos são registrados em `logs/aplicacao.log`:

```
2026-01-15 14:23:45 - INFO - Iniciando processamento de pedidos...
2026-01-15 14:23:46 - INFO - Lendo arquivo: data/exemplo_pedidos.csv
2026-01-15 14:23:47 - INFO - 10 pedidos processados com sucesso
2026-01-15 14:23:48 - INFO - Relatório gerado: output/relatorio_pedidos.xlsx
```

## 🔗 Links Úteis

- [Python Oficial](https://www.python.org)
- [Pandas Documentação](https://pandas.pydata.org)
- [OpenPyXL Documentação](https://openpyxl.readthedocs.io)
- [Schedule Library](https://schedule.readthedocs.io)

## 🤝 Contribuindo

1. Faça um Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido como sistema de automação de pedidos.

---