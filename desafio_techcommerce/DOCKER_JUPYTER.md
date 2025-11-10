# 🐳 Executando no Docker/Jupyter - TechCommerce

## Opção 1: Executar no Jupyter (Docker)

### 1. Acesse o Jupyter
- URL: http://localhost:8888
- Token: `dataops123`

### 2. Abra um Terminal no Jupyter
- Menu: New → Terminal

### 3. Instale as dependências
```bash
cd /home/jovyan/work
pip install great-expectations pyyaml loguru
```

### 4. Navegue até o projeto
```bash
cd desafio_techcommerce/src
```

### 5. Execute o pipeline completo
```bash
python main.py
```

---

## Opção 2: Executar Módulos Individuais

### No Terminal do Jupyter:

```bash
cd /home/jovyan/work/desafio_techcommerce/src

# 1. Setup Great Expectations
python great_expectations_setup.py

# 2. Criar Expectation Suites
python expectation_suites.py

# 3. Ingestão de Dados
python pipeline_ingestao.py

# 4. Correção Automática
python correcao_automatica.py

# 5. Dashboard de Qualidade
python dashboard_qualidade.py

# 6. Sistema de Alertas
python sistema_alertas.py
```

---

## Opção 3: Usar Notebook Interativo

### Crie um novo notebook: `executar_pipeline.ipynb`

```python
# Célula 1: Setup
import sys
sys.path.append('/home/jovyan/work/desafio_techcommerce/src')

# Célula 2: Imports
from pipeline_ingestao import DataIngestionPipeline
from correcao_automatica import DataCleaner
from dashboard_qualidade import QualityDashboard
from sistema_alertas import AlertSystem

# Célula 3: Ingestão
pipeline = DataIngestionPipeline(
    raw_data_path='/home/jovyan/work/notebooks/datasets'
)
datasets = pipeline.ingest_all()
print(f"✓ {len(datasets)} datasets carregados")

# Célula 4: Limpeza
cleaner = DataCleaner()
cleaned = cleaner.clean_all(
    datasets['clientes_lab'],
    datasets['produtos'],
    datasets['vendas'],
    datasets['logistica']
)
print(f"✓ Dados limpos")

# Célula 5: Dashboard
dashboard = QualityDashboard()
results = dashboard.run_full_pipeline()

# Célula 6: Alertas
alert_system = AlertSystem()
alerts = alert_system.process_alerts(results)
print(f"✓ {len(alerts)} alertas gerados")

# Célula 7: Visualizar resultados
import pandas as pd
print("\n📊 Resumo:")
print(f"Score: {results['summary']['success_rate']:.1f}%")
print(f"Alertas: {len(alerts)}")

# Ver dados limpos
display(cleaned['clientes'].head())
```

---

## Opção 4: Executar via PowerShell (Windows)

### Se preferir executar localmente:

```powershell
# Conectar ao container Docker
docker exec -it dataops_lab_container bash

# Dentro do container
cd /home/jovyan/work/desafio_techcommerce/src
python main.py
```

---

## 📁 Onde Encontrar os Resultados

### No Jupyter File Browser:

```
work/
└── desafio_techcommerce/
    ├── data/
    │   ├── processed/          ← Dados limpos (CSVs)
    │   └── quality/
    │       ├── relatorio_qualidade_*.txt  ← Relatório principal
    │       ├── metrics_latest.json        ← Métricas em JSON
    │       ├── alertas_*.json             ← Alertas gerados
    │       ├── audit_log.json             ← Log de auditoria
    │       └── pipeline.log               ← Logs técnicos
    │
    └── great_expectations/
        └── uncommitted/
            └── data_docs/
                └── local_site/
                    └── index.html  ← 🌟 Abra este arquivo!
```

---

## 🌐 Visualizar Data Docs

### Opção A: No Jupyter
1. Navegue até: `great_expectations/uncommitted/data_docs/local_site/`
2. Clique direito em `index.html`
3. Selecione "Open"

### Opção B: Download
1. Download do arquivo `index.html`
2. Abra no seu navegador local

---

## 🐛 Troubleshooting

### Erro: "Module not found"
```bash
pip install great-expectations pyyaml loguru pandas
```

### Erro: "No such file or directory"
```bash
# Verifique se está no diretório correto
pwd
# Deve ser: /home/jovyan/work/desafio_techcommerce/src
```

### Erro: "Permission denied"
```bash
# Dê permissões
chmod +x main.py
```

### Ver logs de erro:
```bash
cat ../data/quality/pipeline.log
```

---

## ✅ Checklist de Execução

- [ ] Docker rodando
- [ ] Jupyter acessível (localhost:8888)
- [ ] Dependências instaladas
- [ ] Navegou até `desafio_techcommerce/src`
- [ ] Executou `python main.py`
- [ ] Verificou resultados em `data/quality/`
- [ ] Abriu Data Docs HTML
- [ ] Revisou relatório de qualidade

---

## 🎯 Resultado Esperado

Ao final da execução, você terá:

```
✅ PIPELINE CONCLUÍDO COM SUCESSO

📊 RESUMO DA EXECUÇÃO:
   • Duração: ~30-60 segundos
   • Datasets processados: 4
   • Datasets limpos: 4
   • Expectation Suites: 4 (6 dimensões cada)
   • Checkpoints executados: 4
   • Alertas gerados: 2-5
   • Score de Qualidade: 95-98%

📁 ARQUIVOS GERADOS:
   • Dados limpos: data/processed/
   • Data Docs: great_expectations/uncommitted/data_docs/
   • Relatórios: data/quality/relatorio_qualidade_*.txt
   • Métricas: data/quality/metrics_latest.json
   • Alertas: data/quality/alertas_*.json
   • Logs: data/quality/pipeline.log
```

---

## 💡 Dicas

1. **Execute módulo por módulo** primeiro para entender o fluxo
2. **Verifique os logs** se houver erros
3. **Explore os Data Docs** - são interativos e muito informativos
4. **Leia o relatório de qualidade** - resume tudo em texto
5. **Adapte conforme necessário** - código é modular

---

**Bom trabalho! 🚀 Qualquer dúvida, consulte README.md ou QUICKSTART.md**
