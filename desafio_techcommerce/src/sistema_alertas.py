"""
Sistema de Alertas - TechCommerce
Monitora qualidade e gera alertas por severidade
"""

import logging
from datetime import datetime
from pathlib import Path
import json
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Severity(Enum):
    """Níveis de severidade de alertas"""
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"
    CRITICAL = "Crítica"


class Alert:
    """Representa um alerta de qualidade"""
    
    def __init__(self, dataset: str, issue: str, severity: Severity, 
                 affected_records: int, total_records: int, details: dict = None):
        self.timestamp = datetime.now()
        self.dataset = dataset
        self.issue = issue
        self.severity = severity
        self.affected_records = affected_records
        self.total_records = total_records
        self.percentage = (affected_records / total_records * 100) if total_records > 0 else 0
        self.details = details or {}
        self.status = "ABERTO"
        
    def to_dict(self):
        """Converte alerta para dicionário"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'dataset': self.dataset,
            'issue': self.issue,
            'severity': self.severity.value,
            'affected_records': self.affected_records,
            'total_records': self.total_records,
            'percentage': round(self.percentage, 2),
            'status': self.status,
            'details': self.details
        }
    
    def __str__(self):
        return (f"[{self.severity.value}] {self.dataset}: {self.issue} "
                f"({self.affected_records}/{self.total_records} = {self.percentage:.1f}%)")


class AlertSystem:
    """Sistema de gerenciamento de alertas"""
    
    def __init__(self, config_path: str = '../config/config.yaml'):
        self.alerts = []
        self.alert_history = []
        self.config_path = Path(config_path)
        
        # Thresholds de severidade (%)
        self.thresholds = {
            Severity.LOW: (1, 3),
            Severity.MEDIUM: (3, 5),
            Severity.HIGH: (5, 10),
            Severity.CRITICAL: (10, 100)
        }
    
    def determine_severity(self, percentage: float) -> Severity:
        """Determina severidade baseada no percentual de problemas"""
        if percentage < 1:
            return None  # Sem alerta
        elif percentage < 3:
            return Severity.LOW
        elif percentage < 5:
            return Severity.MEDIUM
        elif percentage < 10:
            return Severity.HIGH
        else:
            return Severity.CRITICAL
    
    def create_alert(self, dataset: str, issue: str, affected: int, 
                    total: int, details: dict = None) -> Alert:
        """Cria novo alerta"""
        percentage = (affected / total * 100) if total > 0 else 0
        severity = self.determine_severity(percentage)
        
        if severity is None:
            return None  # Não cria alerta para problemas < 1%
        
        alert = Alert(dataset, issue, severity, affected, total, details)
        self.alerts.append(alert)
        
        # Log baseado em severidade
        log_msg = str(alert)
        if severity == Severity.CRITICAL:
            logger.critical(log_msg)
        elif severity == Severity.HIGH:
            logger.error(log_msg)
        elif severity == Severity.MEDIUM:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
        
        return alert
    
    def escalate_alert(self, alert: Alert):
        """Escala alerta para responsáveis"""
        logger.info(f"Escalando alerta: {alert}")
        
        # Determinar destinatários baseado em severidade
        if alert.severity == Severity.CRITICAL:
            recipients = ["CDO", "Data Owner", "Data Steward"]
            sla_hours = 4
        elif alert.severity == Severity.HIGH:
            recipients = ["Data Owner", "Data Steward"]
            sla_hours = 24
        elif alert.severity == Severity.MEDIUM:
            recipients = ["Data Steward"]
            sla_hours = 48
        else:
            recipients = ["Data Custodian"]
            sla_hours = 168
        
        escalation = {
            'alert': alert.to_dict(),
            'recipients': recipients,
            'sla_hours': sla_hours,
            'escalated_at': datetime.now().isoformat()
        }
        
        # Salvar escalação
        self._save_escalation(escalation)
        
        return escalation
    
    def _save_escalation(self, escalation: dict):
        """Salva escalação em arquivo"""
        escalations_path = Path('../data/quality/escalations.json')
        escalations_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(escalations_path, 'a') as f:
            f.write(json.dumps(escalation) + '\n')
    
    def analyze_quality_results(self, results: dict):
        """Analisa resultados de qualidade e gera alertas"""
        logger.info("Analisando resultados de qualidade...")
        
        for checkpoint, details in results.get('checkpoints', {}).items():
            dataset = checkpoint.replace('checkpoint_', '').replace('_lab', '')
            
            if not details.get('success', False):
                # Checkpoint falhou completamente
                self.create_alert(
                    dataset=dataset,
                    issue="Checkpoint falhou completamente",
                    affected=1,
                    total=1,
                    details={'error': details.get('error', 'Unknown')}
                )
        
        # Verificar taxa de sucesso geral
        summary = results.get('summary', {})
        success_rate = summary.get('success_rate', 100)
        failure_rate = 100 - success_rate
        
        if failure_rate > 0:
            self.create_alert(
                dataset="GERAL",
                issue="Taxa de falha nos checkpoints",
                affected=int(summary.get('failed', 0)),
                total=int(summary.get('total', 1)),
                details=summary
            )
    
    def generate_alert_dashboard(self) -> str:
        """Gera dashboard textual de alertas"""
        if not self.alerts:
            return "\n✅ Nenhum alerta ativo - Qualidade dentro dos padrões!\n"
        
        dashboard = "\n" + "=" * 80 + "\n"
        dashboard += "DASHBOARD DE ALERTAS - TECHCOMMERCE\n"
        dashboard += "=" * 80 + "\n"
        dashboard += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        dashboard += f"Total de Alertas Ativos: {len(self.alerts)}\n\n"
        
        # Agrupar por severidade
        by_severity = {}
        for alert in self.alerts:
            severity = alert.severity
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(alert)
        
        # Exibir por severidade (ordem decrescente)
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            alerts = by_severity.get(severity, [])
            if alerts:
                icon = "🔴" if severity == Severity.CRITICAL else \
                       "🟠" if severity == Severity.HIGH else \
                       "🟡" if severity == Severity.MEDIUM else "🟢"
                
                dashboard += f"\n{icon} {severity.value.upper()} ({len(alerts)} alertas):\n"
                dashboard += "-" * 80 + "\n"
                
                for alert in alerts:
                    dashboard += f"  • {alert.dataset}: {alert.issue}\n"
                    dashboard += f"    Afetados: {alert.affected_records}/{alert.total_records} ({alert.percentage:.1f}%)\n"
                    if alert.details:
                        dashboard += f"    Detalhes: {alert.details}\n"
                    dashboard += "\n"
        
        dashboard += "=" * 80 + "\n"
        
        return dashboard
    
    def save_alerts(self, filename: str = None):
        """Salva alertas em arquivo JSON"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"alertas_{timestamp}.json"
        
        output_path = Path('../data/quality') / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        alerts_data = {
            'timestamp': datetime.now().isoformat(),
            'total_alerts': len(self.alerts),
            'alerts': [alert.to_dict() for alert in self.alerts]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dumps(alerts_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Alertas salvos: {output_path}")
        return output_path
    
    def process_alerts(self, results: dict):
        """Processa alertas completos"""
        logger.info("\n" + "=" * 80)
        logger.info("PROCESSANDO ALERTAS")
        logger.info("=" * 80)
        
        # Analisar resultados
        self.analyze_quality_results(results)
        
        # Escalar alertas críticos e altos
        for alert in self.alerts:
            if alert.severity in [Severity.CRITICAL, Severity.HIGH]:
                self.escalate_alert(alert)
        
        # Gerar e exibir dashboard
        dashboard = self.generate_alert_dashboard()
        print(dashboard)
        
        # Salvar alertas
        self.save_alerts()
        
        logger.info("=" * 80)
        logger.info(f"✓ Processamento concluído: {len(self.alerts)} alertas gerados")
        logger.info("=" * 80)
        
        return self.alerts


def main():
    """Função principal"""
    # Exemplo de uso
    alert_system = AlertSystem()
    
    # Simular resultados de qualidade
    mock_results = {
        'checkpoints': {
            'checkpoint_clientes_lab': {'success': False, 'error': 'Duplicatas > 10%'},
            'checkpoint_produtos': {'success': True},
            'checkpoint_vendas': {'success': False, 'error': 'Valores inválidos'},
            'checkpoint_logistica': {'success': True}
        },
        'summary': {
            'total': 4,
            'successful': 2,
            'failed': 2,
            'success_rate': 50.0
        }
    }
    
    # Processar alertas
    alerts = alert_system.process_alerts(mock_results)
    
    print(f"\n🚨 Total de Alertas: {len(alerts)}")


if __name__ == "__main__":
    main()
