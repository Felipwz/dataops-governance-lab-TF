"""
Dashboard de Qualidade - TechCommerce
Gera relatórios e métricas usando Great Expectations Data Docs
"""

import great_expectations as gx
from pathlib import Path
import logging
import json
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityDashboard:
    """Gerencia dashboard de qualidade e Data Docs"""
    
    def __init__(self, config_path: str = '../config/config.yaml'):
        self.config_path = Path(config_path)
        self.context = None
        self.metrics = {}
        
    def initialize(self):
        """Inicializa Great Expectations context"""
        logger.info("Inicializando Dashboard de Qualidade...")
        self.context = gx.get_context()
        return self.context
    
    def run_checkpoint(self, checkpoint_name: str) -> dict:
        """Executa checkpoint e retorna resultados"""
        logger.info(f"Executando checkpoint: {checkpoint_name}")
        
        try:
            results = self.context.run_checkpoint(checkpoint_name=checkpoint_name)
            
            # Extrair métricas
            success = results.success
            stats = {
                'checkpoint': checkpoint_name,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'run_id': str(results.run_id) if hasattr(results, 'run_id') else None
            }
            
            logger.info(f"  ✓ Checkpoint executado: {'SUCESSO' if success else 'FALHA'}")
            return stats
            
        except Exception as e:
            logger.error(f"  ✗ Erro ao executar checkpoint: {str(e)}")
            return {
                'checkpoint': checkpoint_name,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_all_checkpoints(self) -> dict:
        """Executa todos os checkpoints configurados"""
        logger.info("=" * 80)
        logger.info("EXECUTANDO TODOS OS CHECKPOINTS")
        logger.info("=" * 80)
        
        checkpoints = [
            'checkpoint_clientes_lab',
            'checkpoint_produtos',
            'checkpoint_vendas',
            'checkpoint_logistica'
        ]
        
        results = {}
        for checkpoint in checkpoints:
            results[checkpoint] = self.run_checkpoint(checkpoint)
        
        # Calcular taxa de sucesso geral
        total = len(results)
        successful = sum(1 for r in results.values() if r.get('success', False))
        success_rate = (successful / total * 100) if total > 0 else 0
        
        logger.info("=" * 80)
        logger.info(f"RESUMO: {successful}/{total} checkpoints bem-sucedidos ({success_rate:.1f}%)")
        logger.info("=" * 80)
        
        return {
            'checkpoints': results,
            'summary': {
                'total': total,
                'successful': successful,
                'failed': total - successful,
                'success_rate': success_rate,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def generate_data_docs(self):
        """Gera Data Docs do Great Expectations"""
        logger.info("Gerando Data Docs...")
        
        try:
            self.context.build_data_docs()
            logger.info("✓ Data Docs gerados com sucesso")
            
            # Tentar abrir Data Docs no navegador
            try:
                self.context.open_data_docs()
                logger.info("✓ Data Docs abertos no navegador")
            except:
                logger.info("  (Data Docs disponíveis localmente)")
                
        except Exception as e:
            logger.error(f"✗ Erro ao gerar Data Docs: {str(e)}")
    
    def calculate_quality_score(self, results: dict) -> float:
        """Calcula score de qualidade geral (0-100)"""
        success_rate = results['summary']['success_rate']
        
        # Classificação
        if success_rate >= 98:
            quality_level = "EXCELENTE"
        elif success_rate >= 95:
            quality_level = "BOM"
        elif success_rate >= 90:
            quality_level = "ACEITÁVEL"
        else:
            quality_level = "CRÍTICO"
        
        return {
            'score': success_rate,
            'level': quality_level,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_executive_report(self, results: dict) -> str:
        """Gera relatório executivo em texto"""
        quality_score = self.calculate_quality_score(results)
        
        report = f"""
{'=' * 80}
RELATÓRIO EXECUTIVO DE QUALIDADE DE DADOS - TECHCOMMERCE
{'=' * 80}

Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

SCORE GERAL DE QUALIDADE: {quality_score['score']:.1f}% - {quality_score['level']}

RESUMO:
  • Total de Checkpoints: {results['summary']['total']}
  • Bem-sucedidos: {results['summary']['successful']}
  • Falharam: {results['summary']['failed']}
  • Taxa de Sucesso: {results['summary']['success_rate']:.1f}%

DETALHAMENTO POR DATASET:
"""
        
        for checkpoint, details in results['checkpoints'].items():
            dataset = checkpoint.replace('checkpoint_', '').replace('_lab', '')
            status = "✓ OK" if details.get('success', False) else "✗ FALHA"
            report += f"  • {dataset.upper():15} {status}\n"
        
        report += f"\n{'=' * 80}\n"
        report += "RECOMENDAÇÕES:\n"
        
        if quality_score['score'] < 90:
            report += "  ⚠️  URGENTE: Qualidade abaixo do aceitável. Revisar processos.\n"
        elif quality_score['score'] < 95:
            report += "  ⚠️  ATENÇÃO: Qualidade requer melhoria.\n"
        elif quality_score['score'] < 98:
            report += "  ✓  Qualidade boa. Manter monitoramento.\n"
        else:
            report += "  ✓  Excelente qualidade! Manter boas práticas.\n"
        
        report += f"{'=' * 80}\n"
        
        return report
    
    def save_report(self, report: str, filename: str = None):
        """Salva relatório em arquivo"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_qualidade_{timestamp}.txt"
        
        output_path = Path('../data/quality') / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"✓ Relatório salvo: {output_path}")
        return output_path
    
    def run_full_pipeline(self):
        """Executa pipeline completo de qualidade"""
        logger.info("\n" + "=" * 80)
        logger.info("INICIANDO PIPELINE DE QUALIDADE - TECHCOMMERCE")
        logger.info("=" * 80 + "\n")
        
        # 1. Inicializar
        self.initialize()
        
        # 2. Executar checkpoints
        results = self.run_all_checkpoints()
        
        # 3. Gerar Data Docs
        self.generate_data_docs()
        
        # 4. Gerar relatório executivo
        report = self.generate_executive_report(results)
        print("\n" + report)
        
        # 5. Salvar relatório
        self.save_report(report)
        
        # 6. Salvar métricas em JSON
        metrics_path = Path('../data/quality/metrics_latest.json')
        with open(metrics_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"✓ Métricas salvas: {metrics_path}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ PIPELINE DE QUALIDADE CONCLUÍDO")
        logger.info("=" * 80)
        
        return results


def main():
    """Função principal"""
    dashboard = QualityDashboard()
    results = dashboard.run_full_pipeline()
    
    # Exibir score final
    quality_score = dashboard.calculate_quality_score(results)
    print(f"\n🎯 Score de Qualidade: {quality_score['score']:.1f}% - {quality_score['level']}")


if __name__ == "__main__":
    main()
