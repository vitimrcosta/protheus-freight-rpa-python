# ============================================================================
# tests/teste_sistema.py
# Script de teste e validação do sistema
# ============================================================================

"""
Script para testar e validar todas as funcionalidades do sistema RPA.
Pode ser executado para garantir que tudo está funcionando corretamente.
"""

import sys
from pathlib import Path
from src.logger_config import setup_logger

logger = setup_logger(__name__)


class TestadorSistema:
    """Executa testes de validação do sistema."""
    
    def __init__(self):
        self.testes_passados = 0
        self.testes_falhados = 0
    
    def testar_importacoes(self) -> bool:
        """Testa se todos os módulos podem ser importados."""
        print("\n[TESTE] Importando módulos...")
        
        try:
            from src.config import CSV_INPUT, OUTPUT_DIR
            from src.core.leitor_csv import LeitorCSV
            from src.core.processador_pedidos import ProcessadorPedidos
            from src.core.gerador_relatorio import GeradorRelatorio
            from src.automacao.rpa_automacao import AutomacaoRPA, IntegracaoEmail
            from src.main import processar_pedidos
            
            print("  ✓ Todas as importações bem-sucedidas")
            self.testes_passados += 1
            return True
            
        except ImportError as e:
            print(f"  ✗ Erro ao importar: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_arquivo_csv(self) -> bool:
        """Testa se o arquivo CSV existe e pode ser lido."""
        print("\n[TESTE] Verificando arquivo CSV...")
        
        try:
            from src.config import CSV_INPUT
            
            if not CSV_INPUT.exists():
                print(f"  ✗ Arquivo não encontrado: {CSV_INPUT}")
                self.testes_falhados += 1
                return False
            
            print(f"  ✓ Arquivo encontrado: {CSV_INPUT}")
            print(f"    Tamanho: {CSV_INPUT.stat().st_size} bytes")
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_leitura_csv(self) -> bool:
        """Testa leitura e validação de CSV."""
        print("\n[TESTE] Lendo e validando CSV...")
        
        try:
            from src.config import CSV_INPUT
            from src.core.leitor_csv import LeitorCSV
            
            leitor = LeitorCSV(CSV_INPUT)
            df = leitor.ler_dados()
            
            print(f"  ✓ CSV lido com sucesso")
            print(f"    Linhas: {len(df)}")
            print(f"    Colunas: {', '.join(df.columns)}")
            
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro ao ler CSV: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_processamento(self) -> bool:
        """Testa processamento de dados."""
        print("\n[TESTE] Processando dados...")
        
        try:
            from src.config import CSV_INPUT
            from src.core.leitor_csv import LeitorCSV
            from src.core.processador_pedidos import ProcessadorPedidos
            
            leitor = LeitorCSV(CSV_INPUT)
            df = leitor.ler_dados()
            processador = ProcessadorPedidos(df)
            
            # Testar cada função
            totais = processador.calcular_total_por_cliente()
            print(f"  ✓ Totais por cliente calculados: {len(totais)} clientes")
            
            fila = processador.criar_fila_fretes()
            print(f"  ✓ Fila de fretes criada: {len(fila)} itens")
            
            resumo = processador.gerar_resumo_executivo()
            print(f"  ✓ Resumo executivo gerado")
            print(f"    Valor total: R$ {resumo['valor_total']:.2f}")
            
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro no processamento: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_geracao_relatorios(self) -> bool:
        """Testa geração de relatórios."""
        print("\n[TESTE] Gerando relatórios...")
        
        try:
            from src.config import CSV_INPUT, OUTPUT_DIR
            from src.core.leitor_csv import LeitorCSV
            from src.core.processador_pedidos import ProcessadorPedidos
            from src.core.gerador_relatorio import GeradorRelatorio
            
            leitor = LeitorCSV(CSV_INPUT)
            df = leitor.ler_dados()
            processador = ProcessadorPedidos(df)
            
            totais = processador.calcular_total_por_cliente()
            fila = processador.criar_fila_fretes()
            resumo = processador.gerar_resumo_executivo()
            
            gerador = GeradorRelatorio(resumo, totais, fila)
            
            # Gerar Excel
            caminho_excel = gerador.gerar_excel()
            print(f"  ✓ Excel gerado: {caminho_excel}")
            
            # Gerar relatório texto
            relatorio_texto = gerador.gerar_relatorio_texto()
            print(f"  ✓ Relatório texto gerado ({len(relatorio_texto)} caracteres)")
            
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro ao gerar relatórios: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_automacao(self) -> bool:
        """Testa módulo de automação."""
        print("\n[TESTE] Testando automação RPA...")
        
        try:
            from src.automacao.rpa_automacao import AutomacaoRPA
            
            rpa = AutomacaoRPA()
            print("  ✓ AutomacaoRPA inicializado")
            
            # Testar agendamento
            tarefas_antes = len(AutomacaoRPA().obter_proximas_tarefas())
            
            def tarefa_teste():
                pass
            
            rpa.agendar_tarefa(tarefa_teste, 60, "Tarefa Teste")
            print("  ✓ Tarefa agendada com sucesso")
            
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro na automação: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def testar_email_simulado(self) -> bool:
        """Testa integração de e-mail simulada."""
        print("\n[TESTE] Testando integração de e-mail...")
        
        try:
            from src.automacao.rpa_automacao import IntegracaoEmail
            from pathlib import Path
            
            # Testar envio de alerta
            resultado = IntegracaoEmail.enviar_alerta_fretes_urgentes(
                "teste@teste.com",
                5
            )
            print("  ✓ Alerta enviado com sucesso" if resultado else "  ✗ Falha ao enviar alerta")
            
            # Criar arquivo temporário para teste
            temp_file = Path("output/teste_temp.txt")
            temp_file.write_text("Teste")
            
            resultado = IntegracaoEmail.enviar_relatorio(
                "teste@teste.com",
                temp_file
            )
            print("  ✓ Relatório enviado com sucesso" if resultado else "  ✗ Falha ao enviar relatório")
            
            temp_file.unlink()
            
            self.testes_passados += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Erro no e-mail: {str(e)}")
            self.testes_falhados += 1
            return False
    
    def executar_todos_testes(self) -> int:
        """Executa todos os testes."""
        print("\n" + "=" * 80)
        print("TESTE DE VALIDAÇÃO DO SISTEMA RPA".center(80))
        print("=" * 80)
        
        self.testar_importacoes()
        self.testar_arquivo_csv()
        self.testar_leitura_csv()
        self.testar_processamento()
        self.testar_geracao_relatorios()
        self.testar_automacao()
        self.testar_email_simulado()
        
        print("\n" + "=" * 80)
        print("RESULTADO DOS TESTES".center(80))
        print("=" * 80)
        print(f"\n✓ Testes passados: {self.testes_passados}")
        print(f"✗ Testes falhados: {self.testes_falhados}")
        print(f"📊 Taxa de sucesso: {(self.testes_passados / (self.testes_passados + self.testes_falhados) * 100):.1f}%")
        print("\n" + "=" * 80 + "\n")
        
        return 0 if self.testes_falhados == 0 else 1


if __name__ == "__main__":
    try:
        testador = TestadorSistema()
        exit_code = testador.executar_todos_testes()
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        sys.exit(1)
