# ============================================================================
# src/core/gerador_relatorio.py
# Módulo responsável pela geração de relatórios em Excel e PDF
# ============================================================================

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict
from src.logger_config import setup_logger
from src.config import EXCEL_OUTPUT, PDF_OUTPUT, DATA_FORMATO

logger = setup_logger(__name__)

class GeradorRelatorio:
    """Responsável pela geração de relatórios em Excel e PDF."""
    
    def __init__(self, resumo: Dict, totais_cliente: pd.DataFrame, fila_fretes: pd.DataFrame):
        """
        Inicializa o gerador com dados para relatório.
        
        Args:
            resumo: Dicionário com resumo executivo
            totais_cliente: DataFrame com totais por cliente
            fila_fretes: DataFrame com fila de fretes
        """
        self.resumo = resumo
        self.totais_cliente = totais_cliente
        self.fila_fretes = fila_fretes
        logger.info("GeradorRelatorio inicializado")
    
    def gerar_excel(self, caminho_saida: Path = EXCEL_OUTPUT) -> Path:
        """
        Gera relatório em formato Excel com múltiplas abas.
        
        Args:
            caminho_saida: Caminho para salvar o arquivo Excel
            
        Returns:
            Path: Caminho do arquivo gerado
        """
        try:
            logger.info(f"Iniciando geração de relatório Excel: {caminho_saida}")
            
            # Criar escritor Excel
            with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
                
                # Aba 1: Resumo Executivo
                self._criar_aba_resumo(writer)
                
                # Aba 2: Totais por Cliente
                self.totais_cliente.to_excel(
                    writer, 
                    sheet_name='Totais_Cliente',
                    index=False
                )
                logger.info("Aba 'Totais_Cliente' adicionada ao Excel")
                
                # Aba 3: Fila de Fretes
                self.fila_fretes.to_excel(
                    writer,
                    sheet_name='Fila_Fretes',
                    index=False
                )
                logger.info("Aba 'Fila_Fretes' adicionada ao Excel")
            
            logger.info(f"Relatório Excel gerado com sucesso: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório Excel: {str(e)}")
            raise
    
    def _criar_aba_resumo(self, writer):
        """
        Cria a aba de resumo executivo no Excel.
        
        Args:
            writer: ExcelWriter do pandas
        """
        try:
            # Formatar dados do resumo
            resumo_df = pd.DataFrame({
                'Métrica': list(self.resumo.keys()),
                'Valor': list(self.resumo.values())
            })
            
            resumo_df.to_excel(
                writer,
                sheet_name='Resumo_Executivo',
                index=False
            )
            logger.info("Aba 'Resumo_Executivo' adicionada ao Excel")
            
        except Exception as e:
            logger.error(f"Erro ao criar aba resumo: {str(e)}")
            raise
    
    def gerar_relatorio_texto(self) -> str:
        """
        Gera um relatório em formato texto para visualização.
        
        Returns:
            str: Conteúdo do relatório em texto
        """
        try:
            logger.info("Gerando relatório em formato texto")
            
            relatorio = []
            relatorio.append("=" * 80)
            relatorio.append("RELATÓRIO DE PROCESSAMENTO DE PEDIDOS - RPA".center(80))
            relatorio.append("=" * 80)
            relatorio.append("")
            
            # Resumo Executivo
            relatorio.append("📊 RESUMO EXECUTIVO".center(80))
            relatorio.append("-" * 80)
            for chave, valor in self.resumo.items():
                relatorio.append(f"{chave.replace('_', ' ').title():<40} {str(valor):<30}")
            relatorio.append("")
            
            # Top 5 Clientes
            relatorio.append("🏆 TOP 5 CLIENTES (Maior Valor)".center(80))
            relatorio.append("-" * 80)
            top_5 = self.totais_cliente.head(5)
            for idx, row in top_5.iterrows():
                relatorio.append(f"{idx+1}. {row['Cliente']:<40} R$ {row['Total_Valor']:.2f}")
            relatorio.append("")
            
            # Fretes Urgentes
            fretes_urgentes = self.fila_fretes[self.fila_fretes['Status'] == 'URGENTE']
            relatorio.append("⚠️  FRETES URGENTES (Requerem atenção imediata)".center(80))
            relatorio.append("-" * 80)
            if len(fretes_urgentes) > 0:
                for idx, row in fretes_urgentes.iterrows():
                    relatorio.append(f"Seq. {row['Seq_Frete']}: {row['C6_NUM']} - {row['C6_CLIENTE']}")
            else:
                relatorio.append("Nenhum frete urgente no momento")
            relatorio.append("")
            
            relatorio.append("=" * 80)
            relatorio.append(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            relatorio.append("=" * 80)
            
            return "\n".join(relatorio)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório texto: {str(e)}")
            raise
    
    def exibir_relatorio(self):
        """Exibe o relatório em formato texto no console."""
        print(self.gerar_relatorio_texto())
