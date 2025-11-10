"""
Pipeline Principal - TechCommerce DataOps
Executa todo o fluxo de qualidade de dados
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline_ingestao import DataIngestionPipeline
from great_expectations_setup import GreatExpectationsSetup
from expectation_suites import ExpectationSuites
from correcao_automatica import DataCleaner
from dashboard_qualidade import QualityDashboard
from sistema_alertas import AlertSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner(text: str):
    """Imprime banner formatado"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def main():
    """Executa pipeline completo de DataOps"""
    
    start_time = datetime.now()
    
    print_banner("🚀 TECHCOMMERCE DATAOPS PIPELINE - INICIANDO")
    logger.info(f"Início: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # === ETAPA 1: SETUP GREAT EXPECTATIONS ===
        print_banner("📊 ETAPA 1/6: Setup Great Expectations")
        gx_setup = GreatExpectationsSetup()
        context = gx_setup.setup_all()
        logger.info("✓ Great Expectations configurado")
        
        # === ETAPA 2: CRIAR EXPECTATION SUITES ===
        print_banner("🎯 ETAPA 2/6: Criando Expectation Suites (6 Dimensões)")
        suites = ExpectationSuites()
        suites.create_all_suites()
        logger.info("✓ Todas as Expectation Suites criadas")
        
        # === ETAPA 3: INGESTÃO DE DADOS ===
        print_banner("📥 ETAPA 3/6: Ingestão de Dados")
        pipeline = DataIngestionPipeline()
        raw_datasets = pipeline.ingest_all()
        logger.info(f"✓ {len(raw_datasets)} datasets ingeridos")
        
        # === ETAPA 4: CORREÇÃO AUTOMÁTICA ===
        print_banner("🧹 ETAPA 4/6: Correção Automática de Dados")
        cleaner = DataCleaner()
        cleaned_datasets = cleaner.clean_all(
            raw_datasets['clientes_lab'],
            raw_datasets['produtos'],
            raw_datasets['vendas'],
            raw_datasets['logistica']
        )
        cleaner.save_cleaned_data(cleaned_datasets)
        logger.info("✓ Dados limpos e salvos")
        
        # === ETAPA 5: DASHBOARD DE QUALIDADE ===
        print_banner("📈 ETAPA 5/6: Dashboard de Qualidade")
        dashboard = QualityDashboard()
        results = dashboard.run_full_pipeline()
        logger.info("✓ Dashboard gerado")
        
        # === ETAPA 6: SISTEMA DE ALERTAS ===
        print_banner("🚨 ETAPA 6/6: Sistema de Alertas")
        alert_system = AlertSystem()
        alerts = alert_system.process_alerts(results)
        logger.info(f"✓ {len(alerts)} alertas processados")
        
        # === RESUMO FINAL ===
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print_banner("✅ PIPELINE CONCLUÍDO COM SUCESSO")
        
        print("📊 RESUMO DA EXECUÇÃO:")
        print(f"   • Duração: {duration:.2f} segundos")
        print(f"   • Datasets processados: {len(raw_datasets)}")
        print(f"   • Datasets limpos: {len(cleaned_datasets)}")
        print(f"   • Expectation Suites: 4 (6 dimensões cada)")
        print(f"   • Checkpoints executados: 4")
        print(f"   • Alertas gerados: {len(alerts)}")
        print(f"   • Score de Qualidade: {results['summary']['success_rate']:.1f}%")
        
        print("\n📁 ARQUIVOS GERADOS:")
        print("   • Dados limpos: data/processed/")
        print("   • Data Docs: great_expectations/uncommitted/data_docs/")
        print("   • Relatórios: data/quality/relatorio_qualidade_*.txt")
        print("   • Métricas: data/quality/metrics_latest.json")
        print("   • Alertas: data/quality/alertas_*.json")
        print("   • Logs: data/quality/pipeline.log")
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("   1. Revisar Data Docs no navegador")
        print("   2. Analisar relatório de qualidade")
        print("   3. Verificar alertas críticos")
        print("   4. Implementar ações corretivas")
        
        print("\n" + "=" * 80)
        logger.info(f"✓ Pipeline concluído em {duration:.2f}s")
        
        return 0
        
    except Exception as e:
        print_banner("❌ ERRO NO PIPELINE")
        logger.error(f"Pipeline falhou: {str(e)}", exc_info=True)
        print(f"\n❌ Erro: {str(e)}")
        print("\n💡 Verifique:")
        print("   • Arquivos CSV estão em ../notebooks/datasets/")
        print("   • Great Expectations está instalado")
        print("   • Logs em data/quality/pipeline.log")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
