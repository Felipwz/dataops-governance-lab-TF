# 🎯 Desafio Final: DataOps, Governança e Qualidade de Dados com Great Expectations

## 📋 Contexto do Desafio

Você foi contratado como **Data Engineer** pela empresa **TechCommerce**, um e-commerce em crescimento que está enfrentando sérios problemas de qualidade de dados. A empresa possui múltiplas fontes de dados (vendas, clientes, produtos, logística) e precisa implementar uma solução completa de **DataOps** e **Governança de Dados**.

### 🏢 Cenário da Empresa

**TechCommerce** possui:
- 📊 **3 sistemas legados** com dados inconsistentes
- 🛒 **E-commerce** com 50.000 transações/dia
- 👥 **500.000 clientes** cadastrados
- 📦 **10.000 produtos** no catálogo
- 🚚 **Logística** terceirizada com dados externos

### 🚨 Problemas Identificados

1. **Dados duplicados** entre sistemas
2. **Formatos inconsistentes** de datas e valores
3. **Campos obrigatórios vazios** em 15% dos registros
4. **Emails inválidos** em 8% da base de clientes
5. **Produtos sem categoria** definida
6. **Vendas com valores negativos**
7. **Falta de auditoria** e rastreabilidade
8. **Ausência de alertas** para problemas de qualidade

---

## 🎯 Objetivos do Desafio

Você deve criar uma **solução completa de DataOps** que inclua:

### 1. 🏗️ Arquitetura de Governança
- Definir **papéis e responsabilidades**
- Criar **políticas de qualidade de dados**
- Estabelecer **padrões e convenções**

### 2. 🔧 Pipeline de Qualidade Automatizado com Great Expectations
- Implementar **Expectation Suites** para as 6 dimensões da qualidade
- Criar **Checkpoints** para automação de validações
- Desenvolver **Data Docs** para relatórios profissionais
- Implementar **sistema de correção automática**

### 3. 📊 Dashboard de Monitoramento
- Métricas de qualidade em **tempo real**
- **Alertas automáticos** para problemas críticos
- **Relatórios executivos** de governança

### 4. 🔍 Sistema de Auditoria
- **Rastreabilidade completa** (Data Lineage)
- **Logs de operações** detalhados
- **Compliance** com LGPD

---

## 📁 Datasets Fornecidos

Você receberá 4 datasets com problemas intencionais:

### 1. `clientes.csv`
```
id_cliente,nome,email,telefone,data_nascimento,cidade,estado,data_cadastro
1,João Silva,joao@email.com,11999887766,1985-03-15,São Paulo,SP,2023-01-10
2,Maria Santos,,11888776655,1990-07-22,Rio de Janeiro,RJ,2023-01-15
1,João Silva,joao@email.com,11999887766,1985-03-15,São Paulo,SP,2023-01-10
3,Pedro,pedro@invalid,119999,2000-12-01,Belo Horizonte,MG,2023-02-01
4,,ana@email.com,11777665544,1995-05-30,São Paulo,SP,2023-02-10
```

### 2. `produtos.csv`
```
id_produto,nome_produto,categoria,preco,estoque,data_criacao,ativo
101,Smartphone XYZ,Eletrônicos,899.99,50,2023-01-01,true
102,Notebook ABC,,1299.99,25,2023-01-05,true
103,Mouse Gamer,Informática,-29.99,100,2023-01-10,true
104,Teclado Mecânico,Informática,199.99,0,2023-01-15,false
105,Smartphone XYZ,Eletrônicos,899.99,50,2023-01-01,true
```

### 3. `vendas.csv`
```
id_venda,id_cliente,id_produto,quantidade,valor_unitario,valor_total,data_venda,status
1001,1,101,2,899.99,1799.98,2023-03-01,Concluída
1002,2,102,1,1299.99,1299.99,2023-03-02,Pendente
1003,999,103,3,29.99,89.97,2023-03-03,Concluída
1004,1,104,-1,199.99,-199.99,2023-03-04,Cancelada
1005,3,101,1,899.99,899.99,2024-12-31,Processando
```

### 4. `logistica.csv`
```
id_entrega,id_venda,transportadora,data_envio,data_entrega_prevista,data_entrega_real,status_entrega
2001,1001,Correios,2023-03-02,2023-03-05,2023-03-04,Entregue
2002,1002,Transportadora XYZ,2023-03-03,,2023-03-10,Entregue
2003,1003,Correios,2023-03-04,2023-03-07,,Em Trânsito
2004,1004,,,,,Cancelada
```

---

## 🚀 Tarefas do Desafio

### **PARTE 1: Análise e Planejamento**

#### 1.1 Documento de Governança
Crie um documento `governanca_techcommerce.md` contendo:

- **Organograma de Dados**:
  - Data Owner para cada domínio (Clientes, Produtos, Vendas, Logística)
  - Data Stewards responsáveis
  - Data Custodians técnicos

- **Políticas de Qualidade**:
  - Definição de cada dimensão da qualidade para o contexto da empresa
  - Limites aceitáveis (ex: máximo 2% de dados incompletos)
  - Ações corretivas para cada tipo de problema

- **Glossário de Negócios**:
  - Definições claras de termos (ex: "Cliente Ativo", "Venda Válida")
  - Padrões de formato (datas, telefones, emails)
  - Regras de relacionamento entre entidades

#### 1.2 Análise de Problemas 
Crie um notebook `analise_problemas.ipynb` que:

- Carregue todos os datasets
- Identifique **todos os problemas de qualidade** presentes
- Classifique cada problema por **dimensão da qualidade**
- Calcule o **impacto** de cada problema (% de registros afetados)
- Priorize os problemas por **criticidade**

### **PARTE 2: Implementação do Pipeline**

#### 2.1 Pipeline de Ingestão
Crie `pipeline_ingestao.py` que:

- Carregue dados de múltiplas fontes
- Aplique **schema validation** rigoroso
- Implemente **testes de schema** automatizados
- Registre **logs de auditoria** para cada operação
- Trate **erros de formato** e **dados corrompidos**

#### 2.2 Great Expectations - Expectation Suites
Crie `great_expectations_setup.py` implementando:

**Configuração do Data Context**:
```python
def setup_great_expectations_context():
    """
    Configura Data Context do Great Expectations
    Cria datasources para todos os datasets
    """
    pass
```

**Expectation Suite para Clientes**:
```python
def create_clientes_expectations(validator):
    """
    Cria expectativas para dataset de clientes:
    - Completude: id_cliente, nome, email não nulos
    - Unicidade: id_cliente, email únicos
    - Validade: email formato válido, telefone 11 dígitos
    - Consistência: estado 2 caracteres
    """
    validator.expect_column_values_to_not_be_null("id_cliente")
    validator.expect_column_values_to_be_unique("id_cliente")
    validator.expect_column_values_to_match_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")
    # Adicionar mais expectativas...
```

**Expectation Suite para Produtos**:
```python
def create_produtos_expectations(validator):
    """
    Expectativas para produtos:
    - Completude: nome_produto, categoria não nulos
    - Validade: preco > 0, estoque >= 0
    - Consistência: categoria em lista válida
    """
    validator.expect_column_values_to_not_be_null("nome_produto")
    validator.expect_column_values_to_be_between("preco", min_value=0)
    # Adicionar mais expectativas...
```

**Expectation Suite para Vendas**:
```python
def create_vendas_expectations(validator):
    """
    Expectativas para vendas:
    - Integridade referencial: id_cliente e id_produto existem
    - Regras de negócio: valor_total = quantidade × valor_unitario
    - Validade: quantidade > 0, data_venda não futura
    """
    validator.expect_column_values_to_be_between("quantidade", min_value=1)
    validator.expect_column_values_to_be_in_set("status", ["Concluída", "Pendente", "Cancelada"])
    # Adicionar mais expectativas...
```

### **PARTE 3: Correção e Enriquecimento (20 pontos)**

#### 3.1 Sistema de Correção Automática (15 pontos)
Crie `correcao_automatica.py` que:

- **Padronize formatos** (datas, telefones, emails)
- **Remova duplicatas** com lógica inteligente
- **Preencha campos vazios** usando regras de negócio
- **Corrija inconsistências** entre datasets
- **Valide relacionamentos** (foreign keys)

#### 3.2 Enriquecimento de Dados (5 pontos)
Implemente funcionalidades para:

- **Geocodificação** de endereços (simular com dados fictícios)
- **Categorização automática** de produtos
- **Cálculo de métricas** derivadas (idade do cliente, tempo de entrega)
- **Flags de qualidade** por registro

### **PARTE 4: Monitoramento e Alertas (20 pontos)**

#### 4.1 Great Expectations Data Docs e Dashboard (10 pontos)
Crie `dashboard_qualidade.py` que:

- **Configure Data Docs** do Great Expectations
- **Gere relatórios HTML** automaticamente
- **Customize templates** para a TechCommerce
- **Integre métricas** de múltiplos datasets
- **Exporte relatórios** executivos em PDF

#### 4.2 Sistema de Alertas (10 pontos)
Implemente `sistema_alertas.py` com:

- **Alertas em tempo real** para problemas críticos
- **Escalação automática** por severidade
- **Notificações personalizadas** por papel (Owner/Steward/Custodian)
- **Dashboard de alertas** ativos
- **Histórico de incidentes**

---

## 📊 Critérios de Avaliação

### **Excelência Técnica (40%)**
- ✅ Código limpo e bem documentado
- ✅ Uso adequado do PySpark e Great Expectations
- ✅ Expectation Suites bem estruturadas
- ✅ Checkpoints configurados corretamente
- ✅ Data Docs personalizados e informativos
- ✅ Tratamento de erros robusto
- ✅ Performance otimizada

### **Aplicação dos Conceitos (30%)**
- ✅ Implementação correta das 6 dimensões com Great Expectations
- ✅ Aplicação dos princípios DataOps
- ✅ Estrutura de governança bem definida
- ✅ Automação efetiva com Checkpoints
- ✅ Monitoramento contínuo com Data Docs
- ✅ Expectativas versionadas e reutilizáveis

### **Solução de Problemas (20%)**
- ✅ Identificação completa dos problemas
- ✅ Priorização adequada por impacto
- ✅ Soluções criativas e eficazes
- ✅ Prevenção de problemas futuros
- ✅ Escalabilidade da solução

### **Documentação e Apresentação (10%)**
- ✅ Documentação clara e completa
- ✅ Comentários explicativos no código
- ✅ README com instruções de uso
- ✅ Relatório executivo de resultados
- ✅ Apresentação dos resultados

---

## 🎁 Entregáveis

### **Estrutura de Arquivos Esperada:**
```
desafio_techcommerce/
├── docs/
│   ├── governanca_techcommerce.md
│   ├── relatorio_executivo.md
│   └── manual_usuario.md
├── notebooks/
│   ├── analise_problemas.ipynb
│   ├── exploracao_dados.ipynb
│   └── validacao_resultados.ipynb
├── src/
│   ├── pipeline_ingestao.py
│   ├── great_expectations_setup.py
│   ├── expectation_suites.py
│   ├── checkpoints_config.py
│   ├── correcao_automatica.py
│   ├── dashboard_qualidade.py
│   └── sistema_alertas.py
├── great_expectations/
│   ├── expectations/
│   ├── checkpoints/
│   ├── plugins/
│   └── uncommitted/
├── data/
│   ├── raw/          # Dados originais
│   ├── processed/    # Dados processados
│   └── quality/      # Relatórios de qualidade
├── tests/
│   └── test_*.py     # Testes unitários
├── config/
│   └── config.yaml   # Configurações
└── README.md
```

### **Demonstração Final:**
- **Apresentação de 15 minutos** mostrando:
  - Problemas identificados e soluções implementadas
  - Great Expectations Expectation Suites em ação
  - Checkpoints executando validações automaticamente
  - Data Docs com relatórios profissionais
  - Pipeline DataOps funcionando end-to-end
  - Casos de teste com dados reais
  - Benefícios alcançados para a TechCommerce identificados e soluções implementadas
  - Pipeline funcionando end-to-end
  - Dashboard de qualidade em ação
  - Casos de teste com dados reais
  - Benefícios alcançados para a TechCommerce

---

## 🏆 Critérios de Excelência

### **Para nota máxima, sua solução deve:**

1. **Identificar 100% dos problemas** presentes nos datasets
2. **Implementar todas as 6 dimensões** com Great Expectations
3. **Criar Expectation Suites** completas para todos os datasets
4. **Configurar Checkpoints** para automação total
5. **Gerar Data Docs** profissionais e informativos
6. **Demonstrar pipeline DataOps** funcionando end-to-end
7. **Incluir validações cross-dataset** com Great Expectations
8. **Documentar completamente** a solução
9. **Apresentar métricas de melhoria** quantificáveis
10. **Propor evoluções futuras** da solução

### **Pontos Extras (Bônus):**
- 🌟 **Custom Expectations** criadas para regras específicas da TechCommerce (+5 pontos)
- 🌟 **Integração com Airflow** para orquestração de Checkpoints (+5 pontos)
- 🌟 **Profiling automático** com Great Expectations (+4 pontos)
- 🌟 **Alertas Slack/Email** integrados aos Checkpoints (+3 pontos)
- 🌟 **Simulação de streaming** de dados com validações (+3 pontos)
- 🌟 **Compliance LGPD** implementado (+2 pontos)

---

## ⏰ Prazo e Formato de Entrega

### **Prazo:** 7 dias corridos a partir do recebimento

### **Formato de Entrega:**
1. **Repositório Git** com todo o código
2. **Arquivo ZIP** com datasets processados
3. **Vídeo de 5 minutos** demonstrando a solução
4. **Documento PDF** com relatório executivo

### **Apresentação:** Agendada individualmente após entrega

---

## 💡 Dicas de Sucesso

### **Planejamento:**
- 📅 **Dia 1-2**: Análise e documentação de governança
- 📅 **Dia 3-4**: Implementação do pipeline core
- 📅 **Dia 5-6**: Testes, correções e dashboard
- 📅 **Dia 7**: Documentação final e apresentação

### **Técnicas:**
- 🔧 Use **Expectation Suites modulares** e reutilizáveis
- 📊 Configure **Checkpoints** com logging detalhado
- ⚡ Otimize **performance** do Great Expectations com batch sizes
- 🧪 Teste **cenários extremos** com expectativas específicas
- 📝 Documente **expectativas** e suas justificativas de negócio
- 🎯 Use **Data Context** profissionalmente configurado

### **Diferenciação:**
- 🎯 Vá **além das expectativas básicas** - crie Custom Expectations
- 🔍 Demonstre **pensamento crítico** na criação de Expectation Suites
- 💼 Conecte **expectativas técnicas** com **regras de negócio**
- 🚀 Mostre **visão de futuro** com Great Expectations em produção
- 📊 Integre **Data Docs** com dashboards executivos

---

## 🤝 Suporte

### **Canais de Dúvidas:**
- 💬 **Slack**: #desafio-dataops
- 📧 **Email**: professor@techcommerce.com
- 🕐 **Office Hours**: Terças e Quintas, 14h-16h

### **Recursos Adicionais:**
- 📚 **Documentação PySpark**: spark.apache.org/docs
- 🎥 **Vídeos de apoio**: disponíveis no LMS
- 💻 **Ambiente de desenvolvimento**: instruções no README

---

## 🎯 Boa Sorte!

Este desafio foi projetado para testar **todos os conhecimentos** adquiridos durante o curso. Lembre-se:

> **"A qualidade dos dados é a base de todas as decisões inteligentes de negócio"**

Mostre que você domina os conceitos de **DataOps**, **Governança** e **Qualidade de Dados** criando uma solução que a TechCommerce ficaria orgulhosa de usar em produção!

**Que a força dos dados esteja com você!** 🚀📊✨