# Sistema RPA de Processamento de Pedidos

Este projeto automatiza o processamento de pedidos a partir de um arquivo CSV, gera um relatório detalhado em Excel e simula o envio de notificações por e-mail.

## ✨ Funcionalidades

- **Leitura de Dados**: Importa pedidos de um arquivo `.csv`.
- **Análise e Processamento**: Calcula totais por cliente, cria uma fila de fretes com status de urgência e gera um resumo executivo.
- **Geração de Relatório**: Cria um arquivo Excel (`.xlsx`) com três abas:
  1.  `Resumo_Executivo`: Visão geral dos totais.
  2.  `Totais_Cliente`: Detalhes de valor e quantidade por cliente.
  3.  `Fila_Fretes`: Lista de fretes a serem despachados.
- **Automação (RPA)**: Pode ser configurado para rodar o processo automaticamente em intervalos de tempo definidos.
- **Notificações**: Simula o envio de e-mails de alerta para fretes urgentes e o relatório final para a gestão.

## 🚀 Como Usar

### 1. Pré-requisitos

- Python 3.9+
- Git

### 2. Instalação

Clone o repositório, crie um ambiente virtual e instale as dependências.

```bash
# 1. Clone o repositório
git clone https://github.com/vitimrcosta/protheus-freight-rpa-python.git
cd protheus-freight-rpa-python

# 2. Crie e ative o ambiente virtual
# Windows
python -m venv venv
venv\Scripts\activate

# Gitbash
python -m venv venv
source venv/Scripts/activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### 3. Execução

Para executar o processo uma vez:

```bash
python main.py
```

- O script lerá o arquivo `data/exemplo_pedidos.csv`.
- O relatório será salvo em `output/relatorio_pedidos.xlsx`.
- Um log de execução será gravado em `logs/aplicacao.log`.

### 4. Executar Testes

Para verificar a integridade do sistema, rode os testes:

```bash
python run_tests.py
```

## 🔧 Configuração

As principais configurações podem ser ajustadas no arquivo `src/config.py`:

- `CSV_INPUT`: Caminho para o arquivo de dados de entrada.
- `EXECUTAR_AGENDADO`: Mude para `True` para ativar a automação contínua.
- `INTERVALO_MINUTOS`: Intervalo em minutos entre as execuções agendadas.

## 📦 Estrutura do Projeto

```
protheus-freight-rpa-python/
├── src/                # Código-fonte principal
├── data/               # Dados de entrada (CSV)
├── output/             # Relatórios gerados (Excel)
├── logs/               # Logs da aplicação
├── tests/              # Testes automatizados
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências
```

## 👨‍💻 Autor

**Vitimrcosta**
- GitHub: [@vitimrcosta](https://github.com/vitimrcosta)
