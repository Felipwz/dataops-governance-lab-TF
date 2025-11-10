"""
Great Expectations Setup - TechCommerce
Configura Data Context e Datasources
"""

import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GreatExpectationsSetup:
    """Gerencia configuração do Great Expectations"""
    
    def __init__(self, project_root: str = '..'):
        self.project_root = Path(project_root)
        self.data_path = self.project_root / 'notebooks' / 'datasets'
        self.context = None
        
    def initialize_context(self):
        """Inicializa Data Context"""
        logger.info("Inicializando Great Expectations Context...")
        
        try:
            # Tenta usar context existente
            self.context = gx.get_context()
            logger.info("Context existente carregado")
        except:
            # Cria novo context
            logger.info("Criando novo Context")
            self.context = gx.get_context(mode="file")
        
        return self.context
    
    def setup_pandas_datasource(self):
        """Configura datasource Pandas para CSVs"""
        logger.info("Configurando Pandas datasource...")
        
        datasource_name = "pandas_datasource"
        
        try:
            # Verifica se datasource já existe
            self.context.get_datasource(datasource_name)
            logger.info(f"Datasource '{datasource_name}' já existe")
        except:
            # Cria novo datasource
            datasource_config = {
                "name": datasource_name,
                "class_name": "Datasource",
                "execution_engine": {
                    "class_name": "PandasExecutionEngine"
                },
                "data_connectors": {
                    "default_runtime_data_connector": {
                        "class_name": "RuntimeDataConnector",
                        "batch_identifiers": ["default_identifier_name"]
                    },
                    "default_inferred_data_connector": {
                        "class_name": "InferredAssetFilesystemDataConnector",
                        "base_directory": str(self.data_path),
                        "default_regex": {
                            "group_names": ["data_asset_name"],
                            "pattern": "(.*)\\.csv"
                        }
                    }
                }
            }
            
            self.context.add_datasource(**datasource_config)
            logger.info(f"Datasource '{datasource_name}' criado com sucesso")
        
        return datasource_name
    
    def create_expectation_suite(self, suite_name: str) -> str:
        """Cria Expectation Suite"""
        logger.info(f"Criando Expectation Suite: {suite_name}")
        
        try:
            # Verifica se suite já existe
            self.context.get_expectation_suite(suite_name)
            logger.info(f"Suite '{suite_name}' já existe")
        except:
            # Cria nova suite
            self.context.add_expectation_suite(suite_name)
            logger.info(f"Suite '{suite_name}' criada com sucesso")
        
        return suite_name
    
    def get_validator(self, dataset_name: str, suite_name: str):
        """Cria validator para dataset"""
        logger.info(f"Criando validator para {dataset_name}")
        
        batch_request = BatchRequest(
            datasource_name="pandas_datasource",
            data_connector_name="default_inferred_data_connector",
            data_asset_name=dataset_name,
            batch_spec_passthrough=None
        )
        
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=suite_name
        )
        
        return validator
    
    def setup_checkpoint(self, checkpoint_name: str, suite_name: str, dataset_name: str):
        """Configura checkpoint para automação"""
        logger.info(f"Configurando checkpoint: {checkpoint_name}")
        
        checkpoint_config = {
            "name": checkpoint_name,
            "config_version": 1.0,
            "class_name": "SimpleCheckpoint",
            "run_name_template": f"%Y%m%d-%H%M%S-{dataset_name}",
            "validations": [
                {
                    "batch_request": {
                        "datasource_name": "pandas_datasource",
                        "data_connector_name": "default_inferred_data_connector",
                        "data_asset_name": dataset_name,
                    },
                    "expectation_suite_name": suite_name
                }
            ]
        }
        
        try:
            self.context.add_checkpoint(**checkpoint_config)
            logger.info(f"Checkpoint '{checkpoint_name}' criado")
        except:
            logger.info(f"Checkpoint '{checkpoint_name}' já existe")
    
    def setup_all(self):
        """Setup completo do Great Expectations"""
        logger.info("=" * 80)
        logger.info("SETUP GREAT EXPECTATIONS - TECHCOMMERCE")
        logger.info("=" * 80)
        
        # Inicializar context
        self.initialize_context()
        
        # Configurar datasource
        self.setup_pandas_datasource()
        
        # Criar suites para cada dataset
        datasets = {
            'clientes_lab': 'suite_clientes',
            'produtos': 'suite_produtos',
            'vendas': 'suite_vendas',
            'logistica': 'suite_logistica'
        }
        
        for dataset, suite in datasets.items():
            self.create_expectation_suite(suite)
            self.setup_checkpoint(f"checkpoint_{dataset}", suite, dataset)
        
        logger.info("=" * 80)
        logger.info("✓ Setup concluído com sucesso!")
        logger.info("=" * 80)
        
        return self.context


def main():
    """Função principal"""
    setup = GreatExpectationsSetup()
    context = setup.setup_all()
    
    print("\n📊 Great Expectations configurado e pronto para uso!")
    print(f"   - Data Context: {context.root_directory}")
    print(f"   - Datasources: {list(context.list_datasources())}")
    print(f"   - Expectation Suites: {len(context.list_expectation_suites())}")


if __name__ == "__main__":
    main()
