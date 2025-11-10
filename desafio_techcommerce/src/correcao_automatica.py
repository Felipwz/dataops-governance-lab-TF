"""
Sistema de Correção Automática - TechCommerce
Implementa limpeza e padronização de dados
"""

import pandas as pd
import re
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Corrige e padroniza dados automaticamente"""
    
    def __init__(self):
        self.corrections_log = []
    
    def log_correction(self, dataset: str, record_id: any, field: str, 
                      old_value: any, new_value: any, reason: str):
        """Registra correção realizada"""
        self.corrections_log.append({
            'timestamp': datetime.now().isoformat(),
            'dataset': dataset,
            'record_id': record_id,
            'field': field,
            'old_value': str(old_value),
            'new_value': str(new_value),
            'reason': reason
        })
    
    # === CLIENTES ===
    
    def clean_clientes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa e padroniza dados de clientes"""
        logger.info("Limpando dataset Clientes...")
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        # 1. Remover duplicatas (manter mais recente)
        duplicates_before = df_clean.duplicated(subset=['id_cliente']).sum()
        if duplicates_before > 0:
            logger.info(f"  → Removendo {duplicates_before} duplicatas")
            df_clean['data_cadastro'] = pd.to_datetime(df_clean['data_cadastro'], errors='coerce')
            df_clean = df_clean.sort_values('data_cadastro', ascending=False)
            df_clean = df_clean.drop_duplicates(subset=['id_cliente'], keep='first')
        
        # 2. Padronizar telefone (remover caracteres especiais)
        df_clean['telefone'] = df_clean['telefone'].astype(str).apply(
            lambda x: re.sub(r'\D', '', x) if pd.notna(x) else x
        )
        
        # 3. Normalizar email (lowercase)
        df_clean['email'] = df_clean['email'].str.lower().str.strip()
        
        # 4. Validar e corrigir emails
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = ~df_clean['email'].str.match(email_pattern, na=False)
        if invalid_emails.sum() > 0:
            logger.warning(f"  → {invalid_emails.sum()} emails inválidos detectados")
            # Marcar como inválido ao invés de remover
            df_clean.loc[invalid_emails, 'email'] = None
        
        # 5. Padronizar estado (uppercase)
        df_clean['estado'] = df_clean['estado'].str.upper().str.strip()
        
        # 6. Padronizar cidade (title case)
        df_clean['cidade'] = df_clean['cidade'].str.title().str.strip()
        
        # 7. Preencher nomes vazios com "Cliente [ID]"
        nome_vazio = df_clean['nome'].isna() | (df_clean['nome'].str.strip() == '')
        if nome_vazio.sum() > 0:
            logger.info(f"  → Preenchendo {nome_vazio.sum()} nomes vazios")
            df_clean.loc[nome_vazio, 'nome'] = df_clean.loc[nome_vazio, 'id_cliente'].apply(
                lambda x: f"Cliente {x}"
            )
        
        # 8. Validar data de nascimento
        df_clean['data_nascimento'] = pd.to_datetime(df_clean['data_nascimento'], errors='coerce')
        current_year = datetime.now().year
        invalid_birth = (df_clean['data_nascimento'].dt.year < 1900) | \
                       (df_clean['data_nascimento'].dt.year > current_year)
        if invalid_birth.sum() > 0:
            logger.warning(f"  → {invalid_birth.sum()} datas de nascimento inválidas")
            df_clean.loc[invalid_birth, 'data_nascimento'] = None
        
        logger.info(f"  ✓ Clientes: {initial_rows} → {len(df_clean)} linhas")
        return df_clean
    
    # === PRODUTOS ===
    
    def clean_produtos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa e padroniza dados de produtos"""
        logger.info("Limpando dataset Produtos...")
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        # 1. Remover duplicatas completas
        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            logger.info(f"  → Removendo {duplicates} duplicatas")
            df_clean = df_clean.drop_duplicates()
        
        # 2. Corrigir preços negativos (converter para positivo)
        preco_negativo = df_clean['preco'] < 0
        if preco_negativo.sum() > 0:
            logger.warning(f"  → Corrigindo {preco_negativo.sum()} preços negativos")
            df_clean.loc[preco_negativo, 'preco'] = df_clean.loc[preco_negativo, 'preco'].abs()
        
        # 3. Validar estoque (não pode ser negativo)
        estoque_negativo = df_clean['estoque'] < 0
        if estoque_negativo.sum() > 0:
            logger.warning(f"  → Corrigindo {estoque_negativo.sum()} estoques negativos")
            df_clean.loc[estoque_negativo, 'estoque'] = 0
        
        # 4. Preencher categorias vazias com "Sem Categoria"
        categoria_vazia = df_clean['categoria'].isna() | (df_clean['categoria'].str.strip() == '')
        if categoria_vazia.sum() > 0:
            logger.info(f"  → Preenchendo {categoria_vazia.sum()} categorias vazias")
            df_clean.loc[categoria_vazia, 'categoria'] = 'Sem Categoria'
        
        # 5. Padronizar categoria (title case)
        df_clean['categoria'] = df_clean['categoria'].str.title().str.strip()
        
        # 6. Padronizar nome do produto
        df_clean['nome_produto'] = df_clean['nome_produto'].str.strip()
        
        # 7. Padronizar booleano ativo
        df_clean['ativo'] = df_clean['ativo'].astype(str).str.lower()
        df_clean['ativo'] = df_clean['ativo'].map({'true': True, 'false': False})
        
        # 8. Validar data de criação
        df_clean['data_criacao'] = pd.to_datetime(df_clean['data_criacao'], errors='coerce')
        
        logger.info(f"  ✓ Produtos: {initial_rows} → {len(df_clean)} linhas")
        return df_clean
    
    # === VENDAS ===
    
    def clean_vendas(self, df: pd.DataFrame, df_clientes: pd.DataFrame, 
                     df_produtos: pd.DataFrame) -> pd.DataFrame:
        """Limpa e valida dados de vendas com integridade referencial"""
        logger.info("Limpando dataset Vendas...")
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        # 1. Validar integridade referencial - Clientes
        valid_clients = df_clientes['id_cliente'].unique()
        invalid_clients = ~df_clean['id_cliente'].isin(valid_clients)
        if invalid_clients.sum() > 0:
            logger.warning(f"  → {invalid_clients.sum()} vendas com clientes inválidos (removidas)")
            df_clean = df_clean[~invalid_clients]
        
        # 2. Validar integridade referencial - Produtos
        valid_products = df_produtos['id_produto'].unique()
        invalid_products = ~df_clean['id_produto'].isin(valid_products)
        if invalid_products.sum() > 0:
            logger.warning(f"  → {invalid_products.sum()} vendas com produtos inválidos (removidas)")
            df_clean = df_clean[~invalid_products]
        
        # 3. Corrigir quantidade negativa (exceto canceladas)
        not_canceled = df_clean['status'] != 'Cancelada'
        qty_negative = (df_clean['quantidade'] <= 0) & not_canceled
        if qty_negative.sum() > 0:
            logger.warning(f"  → Corrigindo {qty_negative.sum()} quantidades negativas")
            df_clean.loc[qty_negative, 'quantidade'] = df_clean.loc[qty_negative, 'quantidade'].abs()
        
        # 4. Recalcular valor_total (quantidade × valor_unitario)
        df_clean['valor_total_calculado'] = df_clean['quantidade'] * df_clean['valor_unitario']
        difference = (df_clean['valor_total'] - df_clean['valor_total_calculado']).abs()
        inconsistent = difference > 0.01  # tolerância de 1 centavo
        
        if inconsistent.sum() > 0:
            logger.info(f"  → Recalculando {inconsistent.sum()} valores totais inconsistentes")
            df_clean.loc[inconsistent, 'valor_total'] = df_clean.loc[inconsistent, 'valor_total_calculado']
        
        df_clean = df_clean.drop('valor_total_calculado', axis=1)
        
        # 5. Validar data de venda (não pode ser futura)
        df_clean['data_venda'] = pd.to_datetime(df_clean['data_venda'], errors='coerce')
        future_dates = df_clean['data_venda'] > datetime.now()
        if future_dates.sum() > 0:
            logger.warning(f"  → {future_dates.sum()} vendas com datas futuras")
            df_clean.loc[future_dates, 'data_venda'] = datetime.now()
        
        # 6. Padronizar status
        df_clean['status'] = df_clean['status'].str.title().str.strip()
        
        logger.info(f"  ✓ Vendas: {initial_rows} → {len(df_clean)} linhas")
        return df_clean
    
    # === LOGÍSTICA ===
    
    def clean_logistica(self, df: pd.DataFrame, df_vendas: pd.DataFrame) -> pd.DataFrame:
        """Limpa e valida dados de logística"""
        logger.info("Limpando dataset Logística...")
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        # 1. Validar integridade referencial - Vendas
        valid_sales = df_vendas['id_venda'].unique()
        invalid_sales = ~df_clean['id_venda'].isin(valid_sales)
        if invalid_sales.sum() > 0:
            logger.warning(f"  → {invalid_sales.sum()} entregas com vendas inválidas (removidas)")
            df_clean = df_clean[~invalid_sales]
        
        # 2. Converter datas
        date_cols = ['data_envio', 'data_entrega_prevista', 'data_entrega_real']
        for col in date_cols:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        # 3. Padronizar status
        df_clean['status_entrega'] = df_clean['status_entrega'].str.title().str.strip()
        
        # 4. Padronizar transportadora
        df_clean['transportadora'] = df_clean['transportadora'].str.title().str.strip()
        
        # 5. Validar lógica de datas
        # data_entrega_real >= data_envio
        invalid_delivery = (df_clean['data_entrega_real'].notna()) & \
                          (df_clean['data_envio'].notna()) & \
                          (df_clean['data_entrega_real'] < df_clean['data_envio'])
        
        if invalid_delivery.sum() > 0:
            logger.warning(f"  → {invalid_delivery.sum()} datas de entrega inválidas")
        
        logger.info(f"  ✓ Logística: {initial_rows} → {len(df_clean)} linhas")
        return df_clean
    
    # === PIPELINE COMPLETO ===
    
    def clean_all(self, clientes_df, produtos_df, vendas_df, logistica_df):
        """Executa limpeza completa de todos os datasets"""
        logger.info("=" * 80)
        logger.info("INICIANDO LIMPEZA AUTOMATIZADA")
        logger.info("=" * 80)
        
        # Limpar na ordem correta (considerando dependências)
        clientes_clean = self.clean_clientes(clientes_df)
        produtos_clean = self.clean_produtos(produtos_df)
        vendas_clean = self.clean_vendas(vendas_df, clientes_clean, produtos_clean)
        logistica_clean = self.clean_logistica(logistica_df, vendas_clean)
        
        logger.info("=" * 80)
        logger.info("✓ LIMPEZA CONCLUÍDA")
        logger.info("=" * 80)
        
        return {
            'clientes': clientes_clean,
            'produtos': produtos_clean,
            'vendas': vendas_clean,
            'logistica': logistica_clean
        }
    
    def save_cleaned_data(self, cleaned_data: dict, output_path: str = '../data/processed'):
        """Salva datasets limpos"""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for name, df in cleaned_data.items():
            file_path = output_dir / f"{name}_cleaned.csv"
            df.to_csv(file_path, index=False)
            logger.info(f"✓ Salvo: {file_path}")


def main():
    """Função principal"""
    from pathlib import Path
    
    # Carregar dados brutos
    data_path = Path('../notebooks/datasets')
    
    clientes_df = pd.read_csv(data_path / 'clientes_lab.csv')
    produtos_df = pd.read_csv(data_path / 'produtos.csv')
    vendas_df = pd.read_csv(data_path / 'vendas.csv')
    logistica_df = pd.read_csv(data_path / 'logistica.csv')
    
    # Executar limpeza
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_all(clientes_df, produtos_df, vendas_df, logistica_df)
    
    # Salvar dados limpos
    cleaner.save_cleaned_data(cleaned_data)
    
    print("\n📊 Resumo da Limpeza:")
    print(f"   Clientes: {len(clientes_df)} → {len(cleaned_data['clientes'])}")
    print(f"   Produtos: {len(produtos_df)} → {len(cleaned_data['produtos'])}")
    print(f"   Vendas: {len(vendas_df)} → {len(cleaned_data['vendas'])}")
    print(f"   Logística: {len(logistica_df)} → {len(cleaned_data['logistica'])}")


if __name__ == "__main__":
    main()
