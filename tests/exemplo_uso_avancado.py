# ============================================================================
# tests/exemplo_uso_avancado.py
# Exemplos de uso avançado e personalizado do sistema
# ============================================================================

"""
Este arquivo demonstra como usar os módulos de forma programática
e integrar com sistemas externos.
"""

from pathlib import Path
from src.core.leitor_csv import LeitorCSV
from src.core.processador_pedidos import ProcessadorPedidos
from src.core.gerador_relatorio import GeradorRelatorio
from src.automacao.rpa_automacao import AutomacaoRPA, IntegracaoEmail
from src.logger_config import setup_logger

logger = setup_logger(__name__)


def exemplo_1_processamento_basico():
    """Exemplo 1: Processamento básico com personalização."""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: PROCESSAMENTO BÁSICO")
    print("=" * 80)
    
    try:
        # Ler dados
        leitor = LeitorCSV("data/exemplo_pedidos.csv")
        df = leitor.ler_dados()
        print(f"✓ {len(df)} pedidos carregados")
        
        # Processar
        processador = ProcessadorPedidos(df)
        totais = processador.calcular_total_por_cliente()
        
        # Exibir top clientes
        print("\nTop 3 Clientes:")
        for idx, row in totais.head(3).iterrows():
            print(f"  {idx+1}. {row['Cliente']:<30} R$ {row['Total_Valor']:>10.2f}")
            
    except Exception as e:
        logger.error(f"Erro no exemplo 1: {str(e)}")


def exemplo_2_filtrar_fretes():
    """Exemplo 2: Processar e filtrar fretes específicos."""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: FILTRANDO FRETES POR STATUS")
    print("=" * 80)
    
    try:
        leitor = LeitorCSV("data/exemplo_pedidos.csv")
        df = leitor.ler_dados()
        
        processador = ProcessadorPedidos(df)
        fila_fretes = processador.criar_fila_fretes()
        
        # Filtrar por status
        urgentes = fila_fretes[fila_fretes['Status'] == 'URGENTE']
        agendados = fila_fretes[fila_fretes['Status'] == 'AGENDADO']
        
        print(f"\n📍 Fretes urgentes: {len(urgentes)}")
        print(f"📍 Fretes agendados: {len(agendados)}")
        
        if len(urgentes) > 0:
            print("\nPrimeiros 3 fretes urgentes:")
            for idx, row in urgentes.head(3).iterrows():
                print(f"  - {row['C6_NUM']} ({row['C6_CLIENTE']})")
                
    except Exception as e:
        logger.error(f"Erro no exemplo 2: {str(e)}")


def exemplo_3_alertas_customizados():
    """Exemplo 3: Criar alertas customizados."""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: ALERTAS CUSTOMIZADOS")
    print("=" * 80)
    
    try:
        leitor = LeitorCSV("data/exemplo_pedidos.csv")
        df = leitor.ler_dados()
        
        processador = ProcessadorPedidos(df)
        resumo = processador.gerar_resumo_executivo()
        
        # Verificar limite de valor
        limite_alerta = 1000000
        if resumo['valor_total'] > limite_alerta:
            print(f"\n⚠️  ALERTA: Valor total ultrapassa R$ {limite_alerta:,.2f}")
            print(f"   Valor processado: R$ {resumo['valor_total']:,.2f}")
            
            # Simular envio de alerta
            IntegracaoEmail.enviar_alerta_fretes_urgentes(
                destinatario="financeiro@empresa.com",
                num_fretes_urgentes=1
            )
            
    except Exception as e:
        logger.error(f"Erro no exemplo 3: {str(e)}")


def exemplo_4_agendamento_tarefas():
    """Exemplo 4: Demonstrar agendamento de tarefas."""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: AGENDAMENTO DE TAREFAS")
    print("=" * 80)
    
    def minha_tarefa():
        """Tarefa personalizada."""
        print("  → Executando tarefa agendada...")
    
    try:
        rpa = AutomacaoRPA()
        
        # Agendar tarefa de teste
        rpa.agendar_tarefa(
            funcao=minha_tarefa,
            intervalo_minutos=1,
            nome_tarefa="Tarefa de Teste"
        )
        
        print("\n✓ Tarefa agendada para execução a cada 1 minuto")
        print("  Próximas tarefas agendadas:")
        
        for tarefa in rpa.obter_proximas_tarefas():
            print(f"    - {tarefa['tarefa'][:50]}...")
            print(f"      Próxima: {tarefa['proxima_execucao']}")
            
    except Exception as e:
        logger.error(f"Erro no exemplo 4: {str(e)}")


def exemplo_5_exportar_customizado():
    """Exemplo 5: Exportar dados de forma customizada."""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: EXPORTAÇÃO CUSTOMIZADA")
    print("=" * 80)
    
    try:
        leitor = LeitorCSV("data/exemplo_pedidos.csv")
        df = leitor.ler_dados()
        
        processador = ProcessadorPedidos(df)
        
        # Exportar para CSV customizado
        df_export = df[['C6_NUM', 'C6_CLIENTE', 'C6_ENTREG']].copy()
        df_export['Total'] = df['Qtd'] * df['Preço']
        
        caminho = Path("output/pedidos_customizado.csv")
        df_export.to_csv(caminho, index=False, encoding='utf-8')
        
        print(f"\n✓ Arquivo exportado: {caminho}")
        print(f"  Total de linhas: {len(df_export)}")
        
    except Exception as e:
        logger.error(f"Erro no exemplo 5: {str(e)}")


def main():
    """Executa todos os exemplos."""
    print("\n" + "=" * 80)
    print("EXEMPLOS DE USO AVANÇADO DO SISTEMA RPA".center(80))
    print("=" * 80)
    
    exemplo_1_processamento_basico()
    exemplo_2_filtrar_fretes()
    exemplo_3_alertas_customizados()
    exemplo_4_agendamento_tarefas()
    exemplo_5_exportar_customizado()
    
    print("\n" + "=" * 80)
    print("EXEMPLOS CONCLUÍDOS")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
