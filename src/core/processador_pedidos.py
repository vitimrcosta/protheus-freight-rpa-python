# ============================================================================
# src/core/processador_pedidos.py
# Módulo responsável pelo processamento de pedidos e fretes
# ============================================================================

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from src.logger_config import setup_logger
from src.config import DIAS_ANTECEDENCIA_FRETE, DATA_FORMATO

logger = setup_logger(__name__)

class ProcessadorPedidos:
    """Responsável pelo processamento e transformação de dados de pedidos."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o processador com DataFrame de pedidos.
        
        Args:
            df: DataFrame com dados dos pedidos
        """
        self.df = df.copy()
        logger.info("ProcessadorPedidos inicializado")
    
    def calcular_total_por_cliente(self) -> pd.DataFrame:
        """
        Calcula o total (Qtd * Preço) por cliente.
        
        Returns:
            pd.DataFrame: DataFrame com totais agregados por cliente
        """
        try:
            logger.info("Iniciando cálculo de totais por cliente")
            
            # Criar coluna de total do item
            self.df['Total_Item'] = self.df['Qtd'] * self.df['Preço']
            
            # Agrupar por cliente
            totais_cliente = self.df.groupby('C6_CLIENTE').agg({
                'C6_NUM': 'count',          # Quantidade de pedidos
                'Qtd': 'sum',               # Quantidade total de itens
                'Total_Item': 'sum',        # Total em valor
                'C6_ENTREG': 'min'          # Primeira data de embarque
            }).reset_index()
            
            totais_cliente.columns = ['Cliente', 'Num_Pedidos', 'Qtd_Total', 'Total_Valor', 'Primeira_Entreg']
            
            # Ordenar por valor decrescente
            totais_cliente = totais_cliente.sort_values('Total_Valor', ascending=False)
            
            logger.info(f"Totais calculados para {len(totais_cliente)} clientes")
            return totais_cliente
            
        except Exception as e:
            logger.error(f"Erro ao calcular totais por cliente: {str(e)}")
            raise
    
    def criar_fila_fretes(self) -> pd.DataFrame:
        """
        Cria uma fila de fretes baseada na data de embarque.
        Agenda fretes com antecedência configurada.
        
        Returns:
            pd.DataFrame: DataFrame com fila de fretes ordenada por data
        """
        try:
            logger.info("Criando fila de fretes")
            
            # Criar fila de fretes
            fila_fretes = self.df[['C6_NUM', 'C6_CLIENTE', 'Qtd', 'C6_ENTREG']].copy()
            
            # Calcular data de agendamento do frete
            fila_fretes['Data_Agendamento_Frete'] = fila_fretes['C6_ENTREG'] - timedelta(days=DIAS_ANTECEDENCIA_FRETE)
            
            # Definir status
            hoje = datetime.now()
            fila_fretes['Status'] = fila_fretes['Data_Agendamento_Frete'].apply(
                lambda x: 'URGENTE' if x.date() <= hoje.date() else 'AGENDADO'
            )
            
            # Ordenar por data de agendamento
            fila_fretes = fila_fretes.sort_values('Data_Agendamento_Frete')
            
            # Resetar índice e adicionar sequência
            fila_fretes = fila_fretes.reset_index(drop=True)
            fila_fretes.insert(0, 'Seq_Frete', range(1, len(fila_fretes) + 1))
            
            logger.info(f"Fila de fretes criada com {len(fila_fretes)} itens")
            logger.info(f"Fretes urgentes: {(fila_fretes['Status'] == 'URGENTE').sum()}")
            
            return fila_fretes
            
        except Exception as e:
            logger.error(f"Erro ao criar fila de fretes: {str(e)}")
            raise
    
    def gerar_resumo_executivo(self) -> Dict:
        """
        Gera um resumo executivo dos dados processados.
        
        Returns:
            dict: Dicionário com métricas resumidas
        """
        try:
            logger.info("Gerando resumo executivo")
            
            resumo = {
                'data_processamento': datetime.now().strftime(DATA_FORMATO),
                'total_pedidos': len(self.df),
                'total_clientes': self.df['C6_CLIENTE'].nunique(),
                'quantidade_total': self.df['Qtd'].sum(),
                'valor_total': (self.df['Qtd'] * self.df['Preço']).sum(),
                'valor_medio_pedido': (self.df['Qtd'] * self.df['Preço']).mean(),
                'data_primeira_entrega': self.df['C6_ENTREG'].min(),
                'data_ultima_entrega': self.df['C6_ENTREG'].max(),
            }
            
            logger.info(f"Resumo gerado: {resumo['total_pedidos']} pedidos, "
                       f"valor total: R$ {resumo['valor_total']:.2f}")
            
            return resumo
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo executivo: {str(e)}")
            raise
