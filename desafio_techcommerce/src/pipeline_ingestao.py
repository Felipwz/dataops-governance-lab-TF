"""
Pipeline de Ingestão de Dados - TechCommerce
Implementa validação de schema, auditoria e tratamento de erros
"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import json
import hashlib

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../data/quality/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AuditLogger:
    """Gerencia logs de auditoria para rastreabilidade"""
    
    def __init__(self, log_path: str = '../data/quality/audit_log.json'):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
    def log_event(self, event_type: str, dataset: str, details: Dict):
        """Registra evento de auditoria"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'dataset': dataset,
            'details': details
        }
        
        # Append ao arquivo de log
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        logger.info(f"Audit: {event_type} - {dataset}")


class SchemaValidator:
    """Valida schemas dos datasets"""
    
    SCHEMAS = {
        'clientes': {
            'id_cliente': 'int64',
            'nome': 'object',
            'email': 'object',
            'telefone': 'object',
            'data_nascimento': 'object',
            'cidade': 'object',
            'estado': 'object',
            'data_cadastro': 'object'
        },
        'produtos': {
            'id_produto': 'int64',
            'nome_produto': 'object',
            'categoria': 'object',
            'preco': 'float64',
            'estoque': 'int64',
            'data_criacao': 'object',
            'ativo': 'object'
        },
        'vendas': {
            'id_venda': 'int64',
            'id_cliente': 'int64',
            'id_produto': 'int64',
            'quantidade': 'int64',
            'valor_unitario': 'float64',
            'valor_total': 'float64',
            'data_venda': 'object',
            'status': 'object'
        },
        'logistica': {
            'id_entrega': 'int64',
            'id_venda': 'int64',
            'transportadora': 'object',
            'data_envio': 'object',
            'data_entrega_prevista': 'object',
            'data_entrega_real': 'object',
            'status_entrega': 'object'
        }
    }
    
    @classmethod
    def validate(cls, df: pd.DataFrame, dataset_name: str) -> Tuple[bool, List[str]]:
        """
        Valida schema do dataset
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        expected_schema = cls.SCHEMAS.get(dataset_name)
        
        if not expected_schema:
            errors.append(f"Schema desconhecido para dataset: {dataset_name}")
            return False, errors
        
        # Verificar colunas faltantes
        expected_cols = set(expected_schema.keys())
        actual_cols = set(df.columns)
        
        missing_cols = expected_cols - actual_cols
        if missing_cols:
            errors.append(f"Colunas faltantes: {missing_cols}")
        
        extra_cols = actual_cols - expected_cols
        if extra_cols:
            errors.append(f"Colunas extras: {extra_cols}")
        
        # Verificar tipos de dados
        for col, expected_type in expected_schema.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if actual_type != expected_type and not (expected_type == 'object' and actual_type.startswith('object')):
                    logger.warning(f"Tipo diferente em {col}: esperado {expected_type}, encontrado {actual_type}")
        
        is_valid = len(errors) == 0
        return is_valid, errors


class DataIngestionPipeline:
    """Pipeline principal de ingestão de dados"""
    
    def __init__(self, raw_data_path: str = '../notebooks/datasets', 
                 processed_data_path: str = '../data/processed'):
        self.raw_path = Path(raw_data_path)
        self.processed_path = Path(processed_data_path)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        self.auditor = AuditLogger()
        self.validator = SchemaValidator()
        
    def calculate_hash(self, df: pd.DataFrame) -> str:
        """Calcula hash MD5 do dataset para detect alterações"""
        df_string = df.to_csv(index=False)
        return hashlib.md5(df_string.encode()).hexdigest()
    
    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Carrega dataset com tratamento de erro"""
        file_path = self.raw_path / f"{dataset_name}.csv"
        
        try:
            logger.info(f"Carregando dataset: {dataset_name}")
            df = pd.read_csv(file_path)
            
            # Log de auditoria
            self.auditor.log_event(
                event_type='LOAD',
                dataset=dataset_name,
                details={
                    'rows': len(df),
                    'columns': len(df.columns),
                    'hash': self.calculate_hash(df)
                }
            )
            
            return df
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"Arquivo vazio: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Erro ao carregar {dataset_name}: {str(e)}")
            raise
    
    def validate_dataset(self, df: pd.DataFrame, dataset_name: str) -> bool:
        """Valida schema do dataset"""
        logger.info(f"Validando schema: {dataset_name}")
        
        is_valid, errors = self.validator.validate(df, dataset_name)
        
        if not is_valid:
            logger.error(f"Schema inválido para {dataset_name}: {errors}")
            self.auditor.log_event(
                event_type='SCHEMA_ERROR',
                dataset=dataset_name,
                details={'errors': errors}
            )
            return False
        
        logger.info(f"Schema válido: {dataset_name}")
        self.auditor.log_event(
            event_type='SCHEMA_VALID',
            dataset=dataset_name,
            details={'status': 'OK'}
        )
        return True
    
    def basic_quality_check(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """Executa verificações básicas de qualidade"""
        logger.info(f"Verificando qualidade básica: {dataset_name}")
        
        quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_count': df.isnull().sum().to_dict(),
            'null_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            'duplicates': df.duplicated().sum(),
            'duplicate_percentage': round(df.duplicated().sum() / len(df) * 100, 2)
        }
        
        # Log de auditoria
        self.auditor.log_event(
            event_type='QUALITY_CHECK',
            dataset=dataset_name,
            details=quality_report
        )
        
        return quality_report
    
    def save_processed(self, df: pd.DataFrame, dataset_name: str):
        """Salva dataset processado"""
        output_path = self.processed_path / f"{dataset_name}_raw.csv"
        
        try:
            df.to_csv(output_path, index=False)
            logger.info(f"Dataset salvo: {output_path}")
            
            self.auditor.log_event(
                event_type='SAVE',
                dataset=dataset_name,
                details={
                    'path': str(output_path),
                    'rows': len(df),
                    'hash': self.calculate_hash(df)
                }
            )
            
        except Exception as e:
            logger.error(f"Erro ao salvar {dataset_name}: {str(e)}")
            raise
    
    def ingest_all(self) -> Dict[str, pd.DataFrame]:
        """Ingere todos os datasets"""
        datasets = ['clientes_lab', 'produtos', 'vendas', 'logistica']
        loaded_data = {}
        
        for dataset in datasets:
            try:
                # Carregar
                df = self.load_dataset(dataset)
                
                # Validar schema
                if not self.validate_dataset(df, dataset.replace('_lab', '')):
                    logger.warning(f"Schema inválido, mas continuando: {dataset}")
                
                # Quality check
                quality_report = self.basic_quality_check(df, dataset)
                
                # Alertas críticos
                if quality_report['duplicate_percentage'] > 10:
                    logger.critical(f"CRÍTICO: {quality_report['duplicate_percentage']}% duplicatas em {dataset}")
                
                null_critical = [k for k, v in quality_report['null_percentage'].items() if v > 10]
                if null_critical:
                    logger.critical(f"CRÍTICO: > 10% nulos em {dataset}: {null_critical}")
                
                # Salvar
                self.save_processed(df, dataset)
                
                loaded_data[dataset] = df
                logger.info(f"✓ Dataset ingerido com sucesso: {dataset}")
                
            except Exception as e:
                logger.error(f"✗ Falha ao ingerir {dataset}: {str(e)}")
                self.auditor.log_event(
                    event_type='INGESTION_ERROR',
                    dataset=dataset,
                    details={'error': str(e)}
                )
        
        return loaded_data


def main():
    """Função principal"""
    logger.info("=" * 80)
    logger.info("INICIANDO PIPELINE DE INGESTÃO - TECHCOMMERCE")
    logger.info("=" * 80)
    
    pipeline = DataIngestionPipeline()
    
    try:
        datasets = pipeline.ingest_all()
        logger.info(f"\n✓ Pipeline concluído: {len(datasets)} datasets ingeridos")
        
        # Resumo
        print("\n" + "=" * 80)
        print("RESUMO DA INGESTÃO")
        print("=" * 80)
        for name, df in datasets.items():
            print(f"  {name:20} - {len(df):6} linhas x {len(df.columns):2} colunas")
        print("=" * 80)
        
    except Exception as e:
        logger.critical(f"Pipeline falhou: {str(e)}")
        raise


if __name__ == "__main__":
    main()
