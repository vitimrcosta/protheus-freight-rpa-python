# ============================================================================
# src/automacao/rpa_automacao.py
# Módulo responsável pela automação e agendamento de tarefas (RPA conceitual)
# ============================================================================

import schedule
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable
from src.logger_config import setup_logger
from src.config import EXECUTAR_AGENDADO, INTERVALO_MINUTOS

logger = setup_logger(__name__)

class AutomacaoRPA:
    """Gerencia automação e agendamento de tarefas (RPA conceitual)."""
    
    def __init__(self):
        """Inicializa o módulo de automação."""
        self.em_execucao = False
        self.thread_scheduler = None
        logger.info("AutomacaoRPA inicializado")
    
    def agendar_tarefa(
        self,
        funcao: Callable,
        intervalo_minutos: int = INTERVALO_MINUTOS,
        nome_tarefa: str = "Tarefa Agendada"
    ):
        """
        Agenda uma tarefa para execução repetida.
        
        Args:
            funcao: Função a ser executada
            intervalo_minutos: Intervalo em minutos para repetição
            nome_tarefa: Nome descritivo da tarefa
        """
        try:
            logger.info(f"Agendando tarefa: {nome_tarefa} (intervalo: {intervalo_minutos} min)")
            
            # Agendar com schedule
            schedule.every(intervalo_minutos).minutes.do(
                self._executar_com_log,
                funcao,
                nome_tarefa
            )
            
        except Exception as e:
            logger.error(f"Erro ao agendar tarefa: {str(e)}")
            raise
    
    @staticmethod
    def _executar_com_log(funcao: Callable, nome_tarefa: str):
        """
        Executa uma função com logging.
        
        Args:
            funcao: Função a executar
            nome_tarefa: Nome da tarefa
        """
        try:
            logger.info(f"[RPA] Executando: {nome_tarefa}")
            funcao()
            logger.info(f"[RPA] Concluído: {nome_tarefa}")
            
        except Exception as e:
            logger.error(f"[RPA] Erro ao executar {nome_tarefa}: {str(e)}")
    
    def iniciar_scheduler(self, em_background: bool = True):
        """
        Inicia o scheduler de tarefas.
        
        Args:
            em_background: Se True, executa em thread separada
        """
        if self.em_execucao:
            logger.warning("Scheduler já está em execução")
            return
        
        self.em_execucao = True
        
        if em_background:
            logger.info("Iniciando scheduler em background")
            self.thread_scheduler = threading.Thread(
                target=self._loop_scheduler,
                daemon=True
            )
            self.thread_scheduler.start()
        else:
            logger.info("Iniciando scheduler em foreground")
            self._loop_scheduler()
    
    def _loop_scheduler(self):
        """Loop principal do scheduler."""
        logger.info("Loop do scheduler iniciado")
        
        while self.em_execucao:
            try:
                schedule.run_pending()
                time.sleep(1)  # Verificar a cada segundo
                
            except Exception as e:
                logger.error(f"Erro no loop do scheduler: {str(e)}")
    
    def parar_scheduler(self):
        """Para o scheduler."""
        logger.info("Parando scheduler")
        self.em_execucao = False
        
        if self.thread_scheduler and self.thread_scheduler.is_alive():
            self.thread_scheduler.join(timeout=5)
        
        schedule.clear()
        logger.info("Scheduler parado")
    
    def obter_proximas_tarefas(self, limite: int = 10) -> list:
        """
        Retorna as próximas tarefas agendadas.
        
        Args:
            limite: Número máximo de tarefas a retornar
            
        Returns:
            list: Lista das próximas tarefas
        """
        tarefas = []
        for job in schedule.jobs[:limite]:
            proxima_execucao = job.next_run
            tarefas.append({
                'tarefa': str(job.job_func),
                'proxima_execucao': proxima_execucao.strftime('%d/%m/%Y %H:%M:%S')
                if proxima_execucao else 'Não agendado'
            })
        
        return tarefas


# Classe para simular integração com e-mail
class IntegracaoEmail:
    """Simula integração com sistema de e-mail para notificações."""
    
    @staticmethod
    def enviar_relatorio(destinatario: str, caminho_arquivo: Path) -> bool:
        """
        Simula envio de relatório por e-mail.
        
        Args:
            destinatario: E-mail do destinatário
            caminho_arquivo: Caminho do arquivo a enviar
            
        Returns:
            bool: True se simulação bem-sucedida
        """
        try:
            logger.info(f"[EMAIL] Simulando envio para: {destinatario}")
            logger.info(f"[EMAIL] Arquivo: {caminho_arquivo.name}")
            
            # Simulação de envio
            if not caminho_arquivo.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
            
            logger.info(f"[EMAIL] ✓ Relatório enviado com sucesso para {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"[EMAIL] Erro ao enviar relatório: {str(e)}")
            return False
    
    @staticmethod
    def enviar_alerta_fretes_urgentes(
        destinatario: str,
        num_fretes_urgentes: int
    ) -> bool:
        """
        Simula envio de alerta de fretes urgentes.
        
        Args:
            destinatario: E-mail do destinatário
            num_fretes_urgentes: Número de fretes urgentes
            
        Returns:
            bool: True se simulação bem-sucedida
        """
        try:
            logger.info(f"[EMAIL] Enviando alerta para: {destinatario}")
            logger.info(f"[EMAIL] Fretes urgentes: {num_fretes_urgentes}")
            
            mensagem = f"""
            ALERTA DE FRETES URGENTES
            
            Existem {num_fretes_urgentes} fretes que requerem atenção imediata.
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            """
            
            logger.info(f"[EMAIL] ✓ Alerta enviado para {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"[EMAIL] Erro ao enviar alerta: {str(e)}")
            return False
