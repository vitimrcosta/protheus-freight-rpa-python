# ============================================================================
# src/automacao/integracao_email_real.py (OPCIONAL)
# Exemplo de como integrar com e-mail real (Gmail, Outlook, etc)
# ============================================================================

"""
Este arquivo demonstra como implementar envio REAL de e-mail.
Por padrão, o sistema usa simulação. Para usar e-mail real, descomente as linhas
e configure suas credenciais.

IMPORTANTE: Nunca commite senhas no código. Use variáveis de ambiente!
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import os
from src.logger_config import setup_logger

logger = setup_logger(__name__)


class IntegracaoEmailReal:
    """Implementação real de envio de e-mail (opcional)."""
    
    # Configurações - Use variáveis de ambiente para segurança!
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'seu_email@gmail.com')
    EMAIL_SENHA = os.getenv('EMAIL_SENHA', '')  # NUNCA deixe aqui em produção!
    
    @staticmethod
    def enviar_relatorio_real(
        destinatario: str,
        caminho_arquivo: Path,
        assunto: str = "Relatório de Processamento de Pedidos"
    ) -> bool:
        """
        Envia relatório por e-mail REAL (Gmail, Outlook, etc).
        
        Args:
            destinatario: E-mail do destinatário
            caminho_arquivo: Caminho do arquivo para anexar
            assunto: Assunto do e-mail
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            if not IntegracaoEmailReal.EMAIL_SENHA:
                logger.warning("Senha de e-mail não configurada. Use variável de ambiente EMAIL_SENHA")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = IntegracaoEmailReal.EMAIL_REMETENTE
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Corpo do e-mail
            corpo = f"""
            Prezado(a),
            
            Segue em anexo o relatório de processamento de pedidos.
            
            Informações:
            - Arquivo: {caminho_arquivo.name}
            - Data: {Path(caminho_arquivo).stat()}
            
            Atenciosamente,
            Sistema RPA
            """
            
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            
            # Anexar arquivo
            if not caminho_arquivo.exists():
                logger.error(f"Arquivo não encontrado: {caminho_arquivo}")
                return False
            
            anexo = MIMEBase('application', 'octet-stream')
            with open(caminho_arquivo, 'rb') as attachment:
                anexo.set_payload(attachment.read())
            
            encoders.encode_base64(anexo)
            anexo.add_header(
                'Content-Disposition',
                f'attachment; filename= {caminho_arquivo.name}',
            )
            msg.attach(anexo)
            
            # Enviar e-mail
            logger.info(f"Conectando ao servidor SMTP: {IntegracaoEmailReal.SMTP_SERVER}:{IntegracaoEmailReal.SMTP_PORT}")
            
            with smtplib.SMTP(IntegracaoEmailReal.SMTP_SERVER, IntegracaoEmailReal.SMTP_PORT) as server:
                server.starttls()
                server.login(IntegracaoEmailReal.EMAIL_REMETENTE, IntegracaoEmailReal.EMAIL_SENHA)
                server.send_message(msg)
            
            logger.info(f"✓ E-mail enviado com sucesso para: {destinatario}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("Erro de autenticação. Verifique e-mail e senha.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Erro SMTP: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail: {str(e)}")
            return False
    
    @staticmethod
    def enviar_alerta_real(
        destinatario: str,
        num_fretes_urgentes: int,
        assunto: str = "⚠️ ALERTA: Fretes Urgentes Requerem Atenção"
    ) -> bool:
        """
        Envia alerta de fretes urgentes por e-mail REAL.
        
        Args:
            destinatario: E-mail do destinatário
            num_fretes_urgentes: Número de fretes urgentes
            assunto: Assunto do alerta
            
        Returns:
            bool: True se enviado com sucesso
        """
        try:
            if not IntegracaoEmailReal.EMAIL_SENHA:
                logger.warning("Senha de e-mail não configurada")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = IntegracaoEmailReal.EMAIL_REMETENTE
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Corpo com urgência
            corpo = f"""
            ⚠️ ALERTA DE FRETES URGENTES ⚠️
            
            Existem {num_fretes_urgentes} FRETES que requerem atenção IMEDIATA!
            
            Ação necessária:
            1. Verificar fila de fretes no relatório
            2. Contatar fornecedor de logística
            3. Confirmar datas de embarque
            
            Acesse o sistema para mais detalhes.
            
            ---
            Mensagem automática do Sistema RPA
            Não responda este e-mail
            """
            
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
            
            # Enviar
            with smtplib.SMTP(IntegracaoEmailReal.SMTP_SERVER, IntegracaoEmailReal.SMTP_PORT) as server:
                server.starttls()
                server.login(IntegracaoEmailReal.EMAIL_REMETENTE, IntegracaoEmailReal.EMAIL_SENHA)
                server.send_message(msg)
            
            logger.info(f"✓ Alerta enviado para: {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar alerta: {str(e)}")
            return False
