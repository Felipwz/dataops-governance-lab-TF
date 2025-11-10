# 🏢 Governança de Dados - TechCommerce

## 📊 Organograma de Dados

### 1. Data Owners (Proprietários de Dados)

```
┌─────────────────────────────────────────────────────────────┐
│                    Chief Data Officer (CDO)                 │
│                    Maria Silva                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬──────────────┐
        │                  │                  │              │
┌───────▼────────┐ ┌──────▼────────┐ ┌───────▼──────┐ ┌─────▼──────┐
│   Clientes     │ │   Produtos    │ │   Vendas     │ │ Logística  │
│  João Santos   │ │ Ana Costa     │ │ Pedro Lima   │ │ Carlos Dias│
│  (Marketing)   │ │ (Produto)     │ │ (Comercial)  │ │ (Ops)      │
└────────────────┘ └───────────────┘ └──────────────┘ └────────────┘
```

#### Responsabilidades dos Data Owners:
- Definir regras de negócio para seu domínio
- Aprovar políticas de qualidade
- Determinar SLAs de qualidade de dados
- Validar correções e enriquecimentos

### 2. Data Stewards (Administradores de Dados)

| Domínio | Steward | Responsabilidades |
|---------|---------|-------------------|
| **Clientes** | Juliana Ferreira | Garantir completude e validade dos dados de clientes, validar emails, telefones |
| **Produtos** | Roberto Alves | Manter catálogo atualizado, garantir categorização, validar preços |
| **Vendas** | Fernanda Lima | Validar transações, garantir integridade referencial, reconciliação |
| **Logística** | Marcos Souza | Monitorar prazos, validar status, integração com transportadoras |

### 3. Data Custodians (Custodiantes Técnicos)

| Área | Custodian | Responsabilidades |
|------|-----------|-------------------|
| **Engenharia de Dados** | Time DataOps | Implementação de pipelines, automação, monitoramento técnico |
| **Infraestrutura** | Time DevOps | Segurança, backups, disaster recovery, performance |
| **Qualidade** | Time QA | Testes automatizados, validações, auditorias |

---

## 📋 Políticas de Qualidade de Dados

### As 6 Dimensões da Qualidade

#### 1. **Completude** (Completeness)
> **Definição**: Todos os campos obrigatórios devem estar preenchidos.

**Limites Aceitáveis**:
- ✅ **Excelente**: ≤ 1% de dados faltantes
- ⚠️ **Aceitável**: 1-3% de dados faltantes
- ❌ **Crítico**: > 3% de dados faltantes

**Ações Corretivas**:
- Dados faltantes críticos: **Bloquear processamento**
- Dados faltantes não-críticos: **Preencher com valor padrão ou NULL**
- **Log detalhado** para análise de causa raiz
- **Alertar** Data Steward responsável

**Campos Críticos por Domínio**:
- Clientes: id_cliente, nome, email, data_cadastro
- Produtos: id_produto, nome_produto, categoria, preco
- Vendas: id_venda, id_cliente, id_produto, data_venda
- Logística: id_entrega, id_venda, status_entrega

#### 2. **Unicidade** (Uniqueness)
> **Definição**: Registros não devem estar duplicados.

**Limites Aceitáveis**:
- ✅ **Excelente**: 0% de duplicatas
- ⚠️ **Aceitável**: ≤ 0.5% de duplicatas
- ❌ **Crítico**: > 0.5% de duplicatas

**Ações Corretivas**:
- **Identificar duplicatas** por chave primária
- **Manter registro mais recente** (data_cadastro/data_criacao)
- **Merge de informações** quando complementares
- **Arquivar registros removidos** para auditoria

**Chaves de Unicidade**:
- Clientes: id_cliente (PK), email (UK)
- Produtos: id_produto (PK), nome_produto + categoria (UK)
- Vendas: id_venda (PK)
- Logística: id_entrega (PK)

#### 3. **Validade** (Validity)
> **Definição**: Dados devem estar em formato correto e dentro de limites válidos.

**Regras de Validação**:

**Clientes**:
- Email: formato válido (regex: `^[\w\.-]+@[\w\.-]+\.\w+$`)
- Telefone: 10-11 dígitos (formato: `(XX) XXXXX-XXXX`)
- Data nascimento: > 1900 e < data atual
- Estado: 2 caracteres, lista válida (UF brasileiras)

**Produtos**:
- Preço: > 0 e < 1.000.000
- Estoque: ≥ 0 e < 100.000
- Categoria: lista controlada de categorias

**Vendas**:
- Quantidade: > 0
- Valor unitário: > 0
- Data venda: ≤ data atual
- Status: valores controlados ["Concluída", "Pendente", "Cancelada", "Processando"]

**Logística**:
- Data entrega real: ≥ data envio
- Data entrega prevista: ≥ data envio

**Ações Corretivas**:
- **Rejeitar** dados inválidos críticos
- **Normalizar** formatos (telefones, datas)
- **Truncar** valores fora do limite
- **Alertar** quando > 5% de dados inválidos

#### 4. **Consistência** (Consistency)
> **Definição**: Dados devem ser consistentes entre diferentes fontes e ao longo do tempo.

**Regras de Consistência**:
- Vendas.valor_total = quantidade × valor_unitario (tolerância: ±0.01)
- Estado sempre uppercase (SP, RJ, MG)
- Datas em formato ISO 8601 (YYYY-MM-DD)
- Booleanos: true/false (lowercase)

**Ações Corretivas**:
- **Padronizar formatos** automaticamente
- **Recalcular** campos derivados
- **Sincronizar** dados entre sistemas
- **Versionar** alterações para rastreabilidade

#### 5. **Precisão** (Accuracy)
> **Definição**: Dados devem refletir a realidade com exatidão.

**Verificações de Precisão**:
- Endereços: validar CEP existe
- Produtos: preço compatível com mercado (±30%)
- Clientes: idade entre 18-120 anos
- Vendas: valor dentro do perfil do cliente

**Ações Corretivas**:
- **Flags de qualidade** (confiança: alta/média/baixa)
- **Validação manual** para dados suspeitos
- **Enriquecimento** com fontes externas
- **Quarentena** para análise

#### 6. **Atualidade** (Timeliness)
> **Definição**: Dados devem estar atualizados e disponíveis no tempo adequado.

**SLAs de Atualização**:
- Clientes: atualização em < 1 hora
- Produtos: atualização em < 30 minutos
- Vendas: atualização em < 5 minutos (tempo real)
- Logística: atualização em < 15 minutos

**Ações Corretivas**:
- **Alertar** quando SLA violado
- **Priorizar** processamento de dados atrasados
- **Escalar** para infraestrutura se problema sistêmico

---

## 📖 Glossário de Negócios

### Definições de Termos

#### **Cliente Ativo**
- Cliente que realizou pelo menos 1 compra nos últimos 90 dias
- Cadastro completo (nome, email, telefone)
- Email válido e não bounced

#### **Cliente Inativo**
- Sem compras nos últimos 90 dias
- Pode ter cadastro incompleto

#### **Venda Válida**
- Status: "Concluída"
- Quantidade > 0
- Valor total > 0
- Cliente e produto existem
- Data venda ≤ data atual

#### **Venda Cancelada**
- Status: "Cancelada"
- Pode ter valores negativos (estorno)
- Mantida para fins de auditoria

#### **Produto Ativo**
- Campo ativo = true
- Estoque ≥ 0 ou sob encomenda
- Preço > 0
- Categoria definida

#### **Entrega no Prazo**
- data_entrega_real ≤ data_entrega_prevista

#### **Entrega Atrasada**
- data_entrega_real > data_entrega_prevista

---

### Padrões de Formato

#### **Datas**
- **Formato**: YYYY-MM-DD (ISO 8601)
- **Exemplos**: 2023-01-15, 2024-12-31
- **Timezone**: America/Sao_Paulo (BRT/BRST)

#### **Telefones**
- **Formato armazenado**: apenas dígitos (11999887766)
- **Formato exibido**: (11) 99988-7766
- **Validação**: 10 ou 11 dígitos
- **DDD**: 2 dígitos válidos (11-99)

#### **Emails**
- **Formato**: usuario@dominio.com
- **Validação**: RFC 5322 compliant
- **Normalização**: lowercase
- **Verificação**: MX record check (opcional)

#### **CPF** (futuro)
- **Formato armazenado**: 11 dígitos
- **Formato exibido**: XXX.XXX.XXX-XX
- **Validação**: dígitos verificadores

#### **CEP**
- **Formato armazenado**: 8 dígitos
- **Formato exibido**: XXXXX-XXX
- **Validação**: existe nos Correios

#### **Moeda**
- **Formato**: DECIMAL(10,2)
- **Símbolo**: R$ (Real brasileiro)
- **Separadores**: vírgula (decimal), ponto (milhar)
- **Exemplo**: R$ 1.299,99

---

### Regras de Relacionamento

#### **Integridade Referencial**

```
Clientes (1) ──< (N) Vendas
Produtos (1) ──< (N) Vendas
Vendas   (1) ──< (1) Logística
```

**Regras**:
1. Uma venda DEVE ter cliente e produto válidos
2. Uma entrega DEVE ter venda válida
3. Não é permitido deletar cliente com vendas ativas
4. Não é permitido deletar produto com vendas nos últimos 12 meses

#### **Regras de Negócio Cross-Dataset**

**Venda → Cliente**:
- id_cliente deve existir em Clientes
- Cliente deve estar ativo no momento da venda

**Venda → Produto**:
- id_produto deve existir em Produtos
- Produto deve estar ativo no momento da venda
- Estoque deve ser suficiente (se controlado)

**Logística → Venda**:
- id_venda deve existir em Vendas
- Status de venda deve ser "Concluída" ou "Processando"
- Se venda cancelada, logística deve ser cancelada

---

## 🎯 Limites de Qualidade por Severidade

### Classificação de Alertas

| Severidade | Limite | Ação | SLA Resolução |
|------------|--------|------|---------------|
| 🟢 **Baixa** | 1-3% de problemas | Log e monitoramento | 7 dias |
| 🟡 **Média** | 3-5% de problemas | Alerta ao Steward | 48 horas |
| 🟠 **Alta** | 5-10% de problemas | Alerta ao Owner + Steward | 24 horas |
| 🔴 **Crítica** | > 10% de problemas | Bloqueio + escalação CDO | 4 horas |

### Métricas de Qualidade (KPIs)

**Objetivo Estratégico**: Qualidade > 95% em todas as dimensões

| Métrica | Meta | Tolerância |
|---------|------|------------|
| Taxa de Completude | 98% | Min 95% |
| Taxa de Unicidade | 100% | Min 99.5% |
| Taxa de Validade | 97% | Min 95% |
| Taxa de Consistência | 99% | Min 97% |
| Taxa de Precisão | 95% | Min 90% |
| SLA Atualidade | 98% | Min 95% |

---

## 📊 Processo de Governança

### Ciclo de Vida dos Dados

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Ingestão   │ -> │  Validação  │ -> │ Processamento│ -> │ Publicação  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                   │                   │
       v                  v                   v                   v
   Schema Check      Quality Check      Transformação         Data Docs
   Audit Log         Great Expectations  Limpeza              Catalogação
```

### Reuniões de Governança

**Semanal - Data Quality Review**:
- Participantes: Stewards + Custodians
- Duração: 30 minutos
- Pauta: KPIs, incidentes, ações corretivas

**Mensal - Data Governance Council**:
- Participantes: CDO + Owners + Stewards
- Duração: 1 hora
- Pauta: Estratégia, políticas, novos requisitos

**Trimestral - Executive Review**:
- Participantes: C-Level
- Duração: 30 minutos
- Pauta: ROI, riscos, roadmap

---

## 🔒 Compliance e Segurança

### LGPD (Lei Geral de Proteção de Dados)

**Dados Sensíveis**:
- Email: PII - requer consentimento
- Telefone: PII - requer consentimento
- Data nascimento: PII - requer consentimento
- Histórico de compras: dados comportamentais

**Direitos dos Titulares**:
- ✅ Acesso aos dados
- ✅ Correção de dados
- ✅ Exclusão (direito ao esquecimento)
- ✅ Portabilidade

**Retenção de Dados**:
- Clientes ativos: enquanto houver relacionamento
- Clientes inativos: 5 anos após última interação
- Vendas: 5 anos (fiscal) + 1 ano (operacional)
- Logs de auditoria: 7 anos

### Segurança

**Controles de Acesso**:
- Princípio do menor privilégio
- Autenticação MFA para ambientes produtivos
- Segregação de ambientes (dev/qa/prod)

**Auditoria**:
- Todas as operações logadas
- Imutabilidade dos logs
- Retenção mínima: 2 anos

---

## 📈 Melhoria Contínua

### Processo PDCA para Qualidade de Dados

1. **Plan**: Definir métricas e metas de qualidade
2. **Do**: Implementar validações e correções
3. **Check**: Monitorar KPIs e identificar desvios
4. **Act**: Ajustar políticas e processos

### Inovação

**Roadmap**:
- Q1 2025: Implementação Great Expectations + Checkpoints
- Q2 2025: Machine Learning para detecção de anomalias
- Q3 2025: Data Observability integrada
- Q4 2025: Self-service data quality

---

**Versão**: 1.0  
**Data**: Novembro 2025  
**Próxima Revisão**: Fevereiro 2026  
**Aprovado por**: Maria Silva (CDO)
