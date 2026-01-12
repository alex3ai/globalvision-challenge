> 🇺🇸 [Read this document in English](README.md)

# GlobalVision Systems & Data Intern - Take Home Challenge

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Sobre o Projeto

Este projeto apresenta uma análise completa de dados de **Accounts** e **Support Cases** extraídos do Salesforce da GlobalVision. O objetivo é processar, transformar e visualizar dados para gerar insights acionáveis que suportem decisões de negócio estratégicas.

---

## 🎯 Objetivos do Desafio

1. **Exploração de Dados**: Compreender a estrutura e qualidade dos datasets
2. **Processamento SQL**: Utilizar SQL dentro do Python para transformações e agregações
3. **Visualizações**: Criar gráficos que comuniquem insights de forma clara
4. **Business Intelligence**: Propor recomendações baseadas em evidências quantitativas

---

## 📂 Estrutura do Projeto

```
globalvision-data-analysis/
│
├── data/
│   └── raw/
│       ├── accounts_anonymized.json
│       └── support_cases_anonymized.json
│
├── notebooks/
│   ├── analysis_walkthrough.ipynb # Notebook principal (Análise Interativa)
│   └── analysis_walkthrough.py # Script Python (Versão executável)
├── output/
│   └── figures/
│       ├── 01_volume_por_industria.png
│       ├── 02_tempo_resolucao.png
│       ├── 03_distribuicao_status.png
│       ├── 04_tendencia_temporal.png
│       └── 05_matriz_prioridade_status.png
│
├── README.md
└── requirements.txt
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior

### Instalação

1. **Clone o repositório** (ou extraia os arquivos do projeto)

```bash
cd globalvision-data-analysis
```

2. **Crie um ambiente virtual** (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

### Executando a Análise

**Opção 1: Jupyter Notebook (Recomendado)**

```bash
jupyter notebook notebooks/analysis_walkthrough.ipynb
```

Execute todas as células sequencialmente (Menu: Cell > Run All)

**Opção 2: Python Script**

Se preferir rodar como script Python:

```bash
python notebooks/analysis_walkthrough.py
```

---

## 📊 Datasets Utilizados

### 1. `accounts_anonymized.json`
- **Registros**: 1.415 contas
- **Período**: Nov/2007 - Jan/2025
- **Campos-chave**: `account_sfid`, `account_name`, `account_industry`, `account_country`

### 2. `support_cases_anonymized.json`
- **Registros**: 10.000 casos de suporte
- **Período**: Nov/2023 - Jan/2025
- **Campos-chave**: `case_sfid`, `account_sfid`, `case_status`, `case_priority`, `case_severity`

---

## 🔍 KPIs Desenvolvidos

### KPI 1: Performance por Indústria
- Volume total de casos por setor
- Tempo médio de resolução
- Percentual de casos críticos (High + Urgent)

### KPI 2: Análise de Status
- Distribuição de casos por status (Closed, New, Working, etc.)
- Backlog atual (casos abertos)
- Eficiência de resolução

### KPI 3: High-Touch Accounts
- Identificação de contas com alto volume de tickets
- Análise de criticidade por cliente
- Priorização de atendimento VIP

### KPI 4: Tendências Temporais
- Evolução mensal de casos criados vs. fechados
- Variação do tempo médio de resolução
- Sazonalidade e padrões de demanda

---

## 📈 Principais Visualizações

| Gráfico | Descrição | Insight-Chave |
|---------|-----------|---------------|
| **Volume por Indústria** | Barras horizontais mostrando top 10 setores | Pharmaceuticals e IT dominam 45% dos casos |
| **Tempo de Resolução** | Comparação de eficiência entre indústrias | Setor "None" tem 23 dias de MTTR (outlier) |
| **Distribuição de Status** | Pizza com % de casos Closed/Open/Duplicate | 70.4% de taxa de fechamento |
| **Tendência Temporal** | Linha dupla (Volume + Eficiência) | Volume de entrada supera fechamento (Backlog crescente) |
| **Matriz de Prioridade** | Heatmap Prioridade vs. Status | Categoria "High" quase não é utilizada |

---

## 💡 Insights de Negócio

### 🎯 Insight 1: Risco de Concentração ("The Whale Client")

**Problema Identificado:**
- **Cliente Outlier:** O cliente `Customer_900e52a5` (IT) representa **16.5%** de todos os casos.
- **Volume:** 1.650 tickets (7x maior que o 2º colocado).
- **Risco:** Backlog atual de 93 casos ativos, indicando potencial insatisfação/churn.

**Recomendação Estratégica:**
- ✅ Implementar atendimento **White Glove** com Technical Account Manager (TAM) dedicado.
- ✅ Investigar histórico de tickets para criar automação/self-service específico.
- ✅ **Meta:** Reduzir volume de tickets deste cliente em 20% em 3 meses.

---

### 🎯 Insight 2: Ineficiência Operacional (Duplicatas e Priorização)

**Problema Identificado:**
- **20.2% de Desperdício:** 2.015 casos são duplicatas, consumindo tempo precioso de triagem.
- **Priorização Quebrada:** Apenas 2 casos "High" em todo histórico. A triagem é binária: "Normal" ou "Urgent".
- **Gargalo:** Casos novos ("New") têm idade média de 159 dias no backlog.

**Recomendação Estratégica:**
- ✅ Implementar validação de duplicidade no Front-End (UX).
- ✅ Eliminar categoria "High" OU redefinir critérios claros de SLA.
- ✅ **Meta:** Reduzir duplicatas para <5% e limpar o backlog antigo.

---

### 🎯 Insight 3: Dados Órfãos & Hegemonia Farmacêutica

**Problema Identificado:**
- **Blind Spot:** **1.593 casos** (15.9%) sem vínculo com Account (orphan data).
- **Impacto:** Impossibilita análise de receita e ROI do suporte ("voo às cegas").
- **Setor Crítico:** Pharmaceuticals representa 7 das top 15 contas por volume.

**Recomendação Estratégica:**
- ✅ **Curto Prazo:** Força-tarefa (ETL) para recuperar linkagem de casos órfãos.
- ✅ **Médio Prazo:** Criar Squad Especializada em Life Sciences/Pharma.
- ✅ **Meta:** Taxa de dados órfãos < 1% e aumentar CSAT do setor Pharma.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **SQLite3**: Database in-memory para queries SQL
- **Matplotlib & Seaborn**: Visualizações estáticas
- **NumPy**: Operações numéricas
- **Jupyter Notebook**: Ambiente interativo de desenvolvimento

---

## 📦 Dependências (requirements.txt)

```txt
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
numpy>=1.24.0
jupyter>=1.0.0
```

---

## 👤 Autor

**Alex Oliveira Mendes**

📧 Email: [Alex_vips2@hotmail.com]  
💼 LinkedIn: [https://www.linkedin.com/in/alex-mendes-80244b292]  

---

## 📝 Notas de Desenvolvimento

### Desafios Encontrados
1. **Integridade de Dados**: 15.9% dos casos sem `account_sfid` válido
2. **Qualidade de Dados**: Categoria "High" praticamente não utilizada
3. **Outliers**: Cliente único representando 16% do volume total

### Decisões Técnicas
- Criação de conta "UNKNOWN_ACCOUNT" para preservar casos órfãos na análise
- Uso de SQLite in-memory para demonstrar proficiência SQL sem setup externo
- Foco em visualizações exportáveis (PNG 300dpi) para apresentações executivas

---

## 🎓 Aprendizados

- Processamento de dados JSON em escala
- Queries SQL complexas com agregações e JOINs
- Data storytelling através de visualizações
- Tradução de insights técnicos em recomendações de negócio

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um processo seletivo para GlobalVision.  
Código disponível sob licença MIT para fins educacionais.

---

## 🙏 Agradecimentos

Agradeço à equipe da GlobalVision pela oportunidade de demonstrar minhas habilidades técnicas e analíticas através deste desafio estimulante!

---

**Data de Submissão**: Janeiro 2026  
**Tempo de Desenvolvimento**: 1 semana  
**Status**: ✅ Completo e Pronto para Apresentação