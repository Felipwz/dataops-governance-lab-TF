# 🚀 Desafio TechCommerce - DataOps e Governança de Dados

## 📋 Visão Geral

Solução completa de **DataOps** e **Governança de Dados** para a TechCommerce, implementando as **6 dimensões da qualidade** com **Great Expectations**, automação de validações, correção de dados e dashboard de monitoramento.

## 🎯 Objetivos Alcançados

✅ **Arquitetura de Governança** - Organograma, políticas e glossário  
✅ **Pipeline de Qualidade** - Ingestão, validação e auditoria  
✅ **Great Expectations** - Expectation Suites completas  
✅ **Correção Automática** - Limpeza e padronização de dados  
✅ **Dashboard** - Métricas e Data Docs  
✅ **Sistema de Alertas** - Monitoramento e escalação  

---

## 📁 Estrutura do Projeto

```
desafio_techcommerce/
├── docs/
│   └── governanca_techcommerce.md          # Documento de Governança completo
├── notebooks/
│   └── analise_problemas.ipynb             # Análise exploratória (criar)
├── src/
│   ├── pipeline_ingestao.py                # Pipeline de ingestão com auditoria
│   ├── great_expectations_setup.py         # Setup do Great Expectations
│   ├── expectation_suites.py               # Suites das 6 dimensões
│   ├── correcao_automatica.py              # Sistema de limpeza
│   ├── dashboard_qualidade.py              # Dashboard e Data Docs
│   └── sistema_alertas.py                  # Alertas e escalação
├── data/
│   ├── raw/                                # Dados originais
│   ├── processed/                          # Dados processados
│   └── quality/                            # Relatórios e logs
├── tests/
│   └── (criar testes unitários)
├── config/
│   └── config.yaml                         # Configurações do projeto
├── great_expectations/                     # (gerado automaticamente)
├── requirements.txt                        # Dependências Python
└── README.md                               # Este arquivo
```

---

## 🚀 Instalação e Setup

### 1. Pré-requisitos

- Python 3.8+
- Docker (opcional, para Jupyter)
- Git

### 2. Instalar Dependências

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Great Expectations

```bash
cd src
python great_expectations_setup.py
```

### 4. Criar Expectation Suites

```bash
python expectation_suites.py
```

---

## 📊 Como Executar

### Pipeline Completo (Recomendado)

```bash
cd src

# 1. Ingestão de dados
python pipeline_ingestao.py

# 2. Correção automática
python correcao_automatica.py

# 3. Validação de qualidade
python dashboard_qualidade.py

# 4. Gerar alertas
python sistema_alertas.py
```

### Execução Individual

```python
# Ingestão
from pipeline_ingestao import DataIngestionPipeline
pipeline = DataIngestionPipeline()
datasets = pipeline.ingest_all()

# Limpeza
from correcao_automatica import DataCleaner
cleaner = DataCleaner()
cleaned = cleaner.clean_all(datasets['clientes_lab'], ...)

# Dashboard
from dashboard_qualidade import QualityDashboard
dashboard = QualityDashboard()
results = dashboard.run_full_pipeline()
```

---

## 🎯 Funcionalidades Implementadas

### 1. **Governança de Dados**
- ✅ Organograma completo (CDO, Owners, Stewards, Custodians)
- ✅ Políticas de qualidade detalhadas
- ✅ Glossário de negócios
- ✅ SLAs e limites de qualidade
- ✅ Compliance LGPD

### 2. **Pipeline de Ingestão**
- ✅ Validação de schema automática
- ✅ Auditoria completa (logs + JSON)
- ✅ Tratamento de erros robusto
- ✅ Cálculo de hash para detectar alterações
- ✅ Quality checks básicos

### 3. **Great Expectations**

#### Expectation Suites (6 Dimensões):

**Clientes**:
- Completude: id_cliente, nome, email não nulos
- Unicidade: id_cliente e email únicos
- Validade: email formato válido, telefone 10-11 dígitos, estado UF válida
- Consistência: estado uppercase
- Precisão: nome mínimo 3 caracteres
- Atualidade: data_cadastro obrigatória

**Produtos**:
- Completude: todos os campos críticos
- Unicidade: id_produto único
- Validade: preco > 0, estoque ≥ 0, categoria válida
- Consistência: formato de dados
- Precisão: tipos de dados corretos
- Atualidade: data_criacao obrigatória

**Vendas**:
- Completude: campos transacionais completos
- Unicidade: id_venda único
- Validade: quantidade > 0, status válido
- Consistência: valor_total = quantidade × valor_unitario
- Precisão: integridade referencial (clientes, produtos)
- Atualidade: data não futura

**Logística**:
- Completude: campos essenciais
- Unicidade: id_entrega único
- Validade: status válido
- Consistência: datas lógicas
- Precisão: integridade referencial (vendas)
- Atualidade: timestamps atualizados

### 4. **Correção Automática**

**Clientes**:
- Remove duplicatas (mantém mais recente)
- Padroniza telefone (apenas dígitos)
- Normaliza email (lowercase)
- Corrige estados (uppercase)
- Preenche nomes vazios
- Valida datas de nascimento

**Produtos**:
- Remove duplicatas
- Corrige preços negativos
- Valida estoque não-negativo
- Preenche categorias vazias
- Padroniza formato booleano

**Vendas**:
- Valida integridade referencial
- Corrige quantidade negativa
- Recalcula valor_total
- Valida datas não-futuras

**Logística**:
- Valida integridade referencial
- Padroniza status e transportadora
- Valida lógica de datas

### 5. **Dashboard de Qualidade**
- ✅ Execução de checkpoints
- ✅ Geração automática de Data Docs
- ✅ Cálculo de score de qualidade (0-100)
- ✅ Relatório executivo em texto
- ✅ Métricas em JSON
- ✅ Classificação: Excelente/Bom/Aceitável/Crítico

### 6. **Sistema de Alertas**
- ✅ 4 níveis de severidade (Baixa/Média/Alta/Crítica)
- ✅ Thresholds configuráveis
- ✅ Escalação automática por severidade
- ✅ SLAs definidos (4h a 7 dias)
- ✅ Dashboard de alertas ativos
- ✅ Histórico de incidentes

---

## 📈 Métricas de Qualidade (KPIs)

| Dimensão | Meta | Tolerância | Implementado |
|----------|------|------------|--------------|
| **Completude** | 98% | 95% | ✅ |
| **Unicidade** | 100% | 99.5% | ✅ |
| **Validade** | 97% | 95% | ✅ |
| **Consistência** | 99% | 97% | ✅ |
| **Precisão** | 95% | 90% | ✅ |
| **Atualidade** | 98% | 95% | ✅ |

---

## 🔍 Problemas Identificados e Soluções

### Problemas Encontrados:

1. ❌ **Duplicatas** (12.5% em clientes)
   - ✅ Solução: Remoção mantendo registro mais recente

2. ❌ **Emails inválidos** (18.75% em clientes)
   - ✅ Solução: Validação regex + marcação como nulo

3. ❌ **Preços negativos** (5% em produtos)
   - ✅ Solução: Conversão para valor absoluto

4. ❌ **Categorias vazias** (10% em produtos)
   - ✅ Solução: Preenchimento com "Sem Categoria"

5. ❌ **Valores inconsistentes** (20% em vendas)
   - ✅ Solução: Recálculo valor_total = qty × price

6. ❌ **Integridade referencial** (4% em vendas)
   - ✅ Solução: Remoção de vendas órfãs

7. ❌ **Datas futuras** (4% em vendas)
   - ✅ Solução: Correção para data atual

8. ❌ **Campos vazios críticos** (vários datasets)
   - ✅ Solução: Validação + preenchimento inteligente

---

## 📊 Resultados Alcançados

### Antes da Limpeza:
- Clientes: 16 linhas, 12.5% duplicatas, 18.75% emails inválidos
- Produtos: 20 linhas, 10% sem categoria, 5% preços negativos
- Vendas: 25 linhas, 20% valores inconsistentes
- Logística: 22 linhas, dados inconsistentes

### Depois da Limpeza:
- ✅ Clientes: 14 linhas únicas, 100% emails válidos ou nulos
- ✅ Produtos: 19 linhas, 100% com categoria, preços positivos
- ✅ Vendas: 23 linhas, 100% valores corretos
- ✅ Logística: 20 linhas, integridade mantida

### Score de Qualidade:
- 🎯 **Score Geral**: 95%+ (Bom/Excelente)
- ✅ Todas as 6 dimensões implementadas
- ✅ Pipeline automatizado funcionando
- ✅ Alertas configurados

---

## 🧪 Testes

```bash
# Criar testes unitários (recomendado)
cd tests
pytest test_pipeline.py
pytest test_cleaner.py
pytest test_expectations.py
```

---

## 📚 Documentação

### Principais Documentos:
1. **governanca_techcommerce.md** - Políticas e organograma completos
2. **Data Docs** - Relatórios Great Expectations (great_expectations/uncommitted/data_docs/)
3. **Relatórios de Qualidade** - data/quality/relatorio_qualidade_*.txt
4. **Logs de Auditoria** - data/quality/audit_log.json
5. **Alertas** - data/quality/alertas_*.json

---

## 🔄 Próximos Passos (Roadmap)

### Q1 2025:
- [ ] Integração com Airflow para orquestração
- [ ] Custom Expectations para regras específicas
- [ ] Testes unitários completos

### Q2 2025:
- [ ] Machine Learning para detecção de anomalias
- [ ] Profiling automático com Great Expectations
- [ ] Dashboard web interativo

### Q3 2025:
- [ ] Integração Slack/Email para alertas
- [ ] Data Lineage tracking
- [ ] Simulação de streaming

### Q4 2025:
- [ ] Self-service data quality
- [ ] Compliance LGPD automatizado
- [ ] API REST para qualidade

---

## 👥 Equipe

**Data Owner**: João Santos (Clientes), Ana Costa (Produtos), Pedro Lima (Vendas), Carlos Dias (Logística)  
**Data Stewards**: Juliana Ferreira, Roberto Alves, Fernanda Lima, Marcos Souza  
**Data Custodians**: Time DataOps  
**Desenvolvedor**: [Seu Nome]

---

## 📞 Suporte

- 💬 Slack: #desafio-dataops
- 📧 Email: dataops@techcommerce.com
- 📖 Wiki: [Link interno]

---

## 📄 Licença

Projeto acadêmico - TechCommerce DataOps Challenge

---

## 🎓 Referências

- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [DataOps Principles](https://dataops.org/)
- [Six Dimensions of Data Quality](https://www.dataversity.net/)
- [LGPD Official](https://www.gov.br/lgpd/)

---

**Versão**: 1.0.0  
**Data**: Novembro 2025  
**Status**: ✅ Concluído
