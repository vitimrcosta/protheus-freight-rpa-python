# ============================================================================
# src/main.py
# Script principal que orquestra todo o fluxo de processamento
# ============================================================================

import sys
import os

# Configurar encoding para UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import time
from pathlib import Path
from datetime import datetime

# Importar módulos do projeto
from src.config import CSV_INPUT, EXECUTAR_AGENDADO, INTERVALO_MINUTOS
from src.logger_config import setup_logger
from src.core.leitor_csv import LeitorCSV
from src.core.processador_pedidos import ProcessadorPedidos
from src.core.gerador_relatorio import GeradorRelatorio
from src.automacao.rpa_automacao import AutomacaoRPA, IntegracaoEmail

logger = setup_logger(__name__)

def processar_pedidos():
    """
    Função principal que executa todo o pipeline de processamento.
    
    Returns:
        bool: True se processamento bem-sucedido, False caso contrário
    """
    try:
        logger.info("=" * 80)
        logger.info("INICIANDO PROCESSAMENTO DE PEDIDOS")
        logger.info("=" * 80)
        
        # Passo 1: Ler dados do CSV
        logger.info("[1/5] Lendo dados do arquivo CSV...")
        leitor = LeitorCSV(CSV_INPUT)
        df = leitor.ler_dados()
        
        # Passo 2: Processar dados
        logger.info("[2/5] Processando dados de pedidos...")
        processador = ProcessadorPedidos(df)
        
        # Calcular totais por cliente
        totais_cliente = processador.calcular_total_por_cliente()
        
        # Criar fila de fretes
        fila_fretes = processador.criar_fila_fretes()
        
        # Gerar resumo executivo
        resumo = processador.gerar_resumo_executivo()
        
        # Passo 3: Gerar relatórios
        logger.info("[3/5] Gerando relatórios...")
        gerador = GeradorRelatorio(resumo, totais_cliente, fila_fretes)
        
        # Gerar Excel
        caminho_excel = gerador.gerar_excel()
        logger.info(f"✓ Relatório Excel gerado: {caminho_excel}")
        
        # Exibir relatório em texto
        logger.info("[4/5] Exibindo relatório executivo...")
        gerador.exibir_relatorio()
        
        # Passo 5: Integração com e-mail (simulated)
        logger.info("[5/5] Simulando integração com e-mail...")
        
        # Contar fretes urgentes
        fretes_urgentes = fila_fretes[fila_fretes['Status'] == 'URGENTE']
        num_urgentes = len(fretes_urgentes)
        
        # Simular envio de alertas
        if num_urgentes > 0:
            IntegracaoEmail.enviar_alerta_fretes_urgentes(
                destinatario="gerencia@empresa.com",
                num_fretes_urgentes=num_urgentes
            )
        
        # Simular envio do relatório
        IntegracaoEmail.enviar_relatorio(
            destinatario="direcao@empresa.com",
            caminho_arquivo=caminho_excel
        )
        
        logger.info("=" * 80)
        logger.info("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 80)
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Erro: Arquivo não encontrado - {str(e)}")
        print(f"\n❌ ERRO: {str(e)}")
        return False
        
    except ValueError as e:
        logger.error(f"Erro: Dados inválidos - {str(e)}")
        print(f"\n❌ ERRO: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        print(f"\n❌ ERRO INESPERADO: {str(e)}")
        return False


def main():
    """Função de entrada do programa."""
    try:
        print("\n" + "=" * 80)
        print("SISTEMA DE AUTOMAÇÃO DE PROCESSAMENTO DE PEDIDOS (RPA)".center(80))
        print("=" * 80 + "\n")
        
        # Executar processamento único
        sucesso = processar_pedidos()
        
        if not sucesso:
            sys.exit(1)
        
        # Se configurado, iniciar agendador de tarefas
        if EXECUTAR_AGENDADO:
            print("\n" + "=" * 80)
            print("INICIANDO AUTOMAÇÃO CONTÍNUA (RPA)".center(80))
            print("=" * 80 + "\n")
            
            rpa = AutomacaoRPA()
            
            # Agendar processamento periódico
            rpa.agendar_tarefa(
                funcao=processar_pedidos,
                intervalo_minutos=INTERVALO_MINUTOS,
                nome_tarefa="Processamento Periódico de Pedidos"
            )
            
            logger.info(f"Tarefas agendadas para execução a cada {INTERVALO_MINUTOS} minutos")
            print(f"\n✓ Automação agendada a cada {INTERVALO_MINUTOS} minutos")
            print("  Pressione CTRL+C para interromper...\n")
            
            # Iniciar scheduler
            rpa.iniciar_scheduler(em_background=False)
            
        else:
            print("\n✓ Processamento executado com sucesso!")
            print("  Para ativar automação contínua, altere EXECUTAR_AGENDADO=True em src/config.py\n")
    
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário")
        print("\n\n⚠️  Execução interrompida pelo usuário")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        print(f"\n❌ ERRO FATAL: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
