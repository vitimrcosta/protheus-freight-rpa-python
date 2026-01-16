# ============================================================================
# src/core/leitor_csv.py
# Módulo responsável pela leitura e validação do arquivo CSV
# ============================================================================

import pandas as pd
from typing import List, Dict, Tuple
from pathlib import Path
from src.logger_config import setup_logger

logger = setup_logger(__name__)

class LeitorCSV:
    """Responsável pela leitura e validação de arquivos CSV de pedidos."""
    
    def __init__(self, caminho_arquivo: Path):
        """
        Inicializa o leitor com caminho do arquivo.
        
        Args:
            caminho_arquivo: Path do arquivo CSV
            
        Raises:
            FileNotFoundError: Se arquivo não existir
        """
        self.caminho_arquivo = Path(caminho_arquivo)
        
        if not self.caminho_arquivo.exists():
            logger.error(f"Arquivo não encontrado: {self.caminho_arquivo}")
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {self.caminho_arquivo}")
        
        logger.info(f"LeitorCSV inicializado com arquivo: {self.caminho_arquivo}")
    
    def ler_dados(self) -> pd.DataFrame:
        """
        Lê e valida os dados do arquivo CSV.
        
        Returns:
            pd.DataFrame: DataFrame com dados validados
            
        Raises:
            ValueError: Se arquivo estiver vazio ou sem colunas obrigatórias
        """
        try:
            logger.info("Iniciando leitura do arquivo CSV")
            df = pd.read_csv(self.caminho_arquivo, encoding='utf-8')
            
            # Validar se possui dados
            if df.empty:
                raise ValueError("Arquivo CSV está vazio")
            
            # Validar colunas obrigatórias
            colunas_obrigatorias = ['C6_NUM', 'C6_CLIENTE', 'C6_ENTREG', 'Qtd', 'Preço']
            colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
            
            if colunas_faltantes:
                raise ValueError(f"Colunas obrigatórias faltando: {colunas_faltantes}")
            
            # Limpar e preparar dados
            df = self._limpar_dados(df)
            
            logger.info(f"Arquivo lido com sucesso. Total de linhas: {len(df)}")
            return df
            
        except pd.errors.ParserError as e:
            logger.error(f"Erro ao fazer parse do CSV: {str(e)}")
            raise ValueError(f"Erro ao ler arquivo CSV: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao ler CSV: {str(e)}")
            raise
    
    @staticmethod
    def _limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza limpeza e normalização dos dados.
        
        Args:
            df: DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame limpo
        """
        try:
            # Remover espaços em branco nas colunas string
            str_columns = df.select_dtypes(include=['object']).columns
            df[str_columns] = df[str_columns].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
            
            # Converter colunas numéricas
            df['Qtd'] = pd.to_numeric(df['Qtd'], errors='coerce')
            df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
            
            # Converter datas
            df['C6_ENTREG'] = pd.to_datetime(df['C6_ENTREG'], format='%d/%m/%Y', errors='coerce')
            
            # Remover linhas com valores inválidos
            linhas_antes = len(df)
            df = df.dropna(subset=['Qtd', 'Preço', 'C6_ENTREG'])
            linhas_removidas = linhas_antes - len(df)
            
            if linhas_removidas > 0:
                logger.warning(f"Removidas {linhas_removidas} linhas com dados inválidos")
            
            logger.info("Dados limpos e normalizados com sucesso")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao limpar dados: {str(e)}")
            raise
