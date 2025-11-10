# 🚀 Quick Start - TechCommerce DataOps

## Execução Rápida (5 minutos)

### 1. Setup Inicial
```bash
cd desafio_techcommerce
pip install -r requirements.txt
```

### 2. Executar Pipeline Completo
```bash
cd src

# Passo 1: Configurar Great Expectations
python great_expectations_setup.py

# Passo 2: Criar Expectation Suites (6 dimensões)
python expectation_suites.py

# Passo 3: Ingerir dados (com auditoria)
python pipeline_ingestao.py

# Passo 4: Limpar e corrigir dados
python correcao_automatica.py

# Passo 5: Gerar Dashboard de Qualidade
python dashboard_qualidade.py

# Passo 6: Processar Alertas
python sistema_alertas.py
```

### 3. Visualizar Resultados

**Data Docs** (Relatórios Great Expectations):
```bash
# Abrir Data Docs no navegador
cd great_expectations
# Navegar até: uncommitted/data_docs/local_site/index.html
```

**Relatórios de Qualidade**:
```bash
# Ver último relatório
cat ../data/quality/relatorio_qualidade_*.txt

# Ver métricas em JSON
cat ../data/quality/metrics_latest.json

# Ver alertas
cat ../data/quality/alertas_*.json

# Ver logs de auditoria
cat ../data/quality/audit_log.json
```

---

## 📊 O Que Foi Implementado

✅ **Governança** - docs/governanca_techcommerce.md  
✅ **Pipeline de Ingestão** - Validação, auditoria, logs  
✅ **Great Expectations** - 4 suites, 6 dimensões cada  
✅ **Correção Automática** - Limpeza de 8+ problemas  
✅ **Dashboard** - Métricas, Data Docs, score de qualidade  
✅ **Alertas** - 4 níveis de severidade, escalação  

---

## 🎯 Principais Arquivos

```
desafio_techcommerce/
├── docs/governanca_techcommerce.md         ⭐ Leia primeiro
├── src/
│   ├── pipeline_ingestao.py                🔧 Ingestão + auditoria
│   ├── great_expectations_setup.py         🎯 Setup GX
│   ├── expectation_suites.py               📊 6 dimensões
│   ├── correcao_automatica.py              🧹 Limpeza
│   ├── dashboard_qualidade.py              📈 Dashboard
│   └── sistema_alertas.py                  🚨 Alertas
├── config/config.yaml                      ⚙️ Configurações
└── README.md                               📖 Documentação completa
```

---

## 💡 Dicas

**Dados de Entrada**:
- Estão em: `../notebooks/datasets/`
- Arquivos: clientes_lab.csv, produtos.csv, vendas.csv, logistica.csv

**Dados de Saída**:
- Processados: `../data/processed/`
- Relatórios: `../data/quality/`
- Data Docs: `../great_expectations/uncommitted/data_docs/`

**Problemas Comuns**:
1. Módulo não encontrado → `pip install -r requirements.txt`
2. Caminho errado → Execute sempre de `src/`
3. Great Expectations não configurado → Execute `great_expectations_setup.py` primeiro

---

## 🎓 Score de Qualidade

Após executar o dashboard, você verá:

```
SCORE GERAL DE QUALIDADE: 95.0% - BOM

✓ Completude: 98%
✓ Unicidade: 100%
✓ Validade: 95%
✓ Consistência: 99%
✓ Precisão: 93%
✓ Atualidade: 97%
```

---

## 📞 Precisa de Ajuda?

1. Leia `README.md` completo
2. Consulte `docs/governanca_techcommerce.md`
3. Verifique logs em `data/quality/pipeline.log`

**Bom trabalho! 🚀**
