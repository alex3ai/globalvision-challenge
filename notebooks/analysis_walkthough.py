# %% [markdown]
# Ingestão e Exploração dos Dados
# 
# Configuração Inicial

# %%
# Célula 1: Imports e Configurações
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configurações visuais
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams['figure.figsize'] = (14, 7)
plt.rcParams['font.size'] = 11

print("✅ Bibliotecas importadas com sucesso!")

# %% [markdown]
# Carregamento dos Dados

# %%
# Célula 2: Carregamento dos JSONs
df_accounts = pd.read_json('../data/raw/accounts_anonymized.json')
df_cases = pd.read_json('../data/raw/support_cases_anonymized.json')

# Converter colunas de data imediatamente (JSON carrega datas como strings)
# Isso facilita o trabalho com SQL mais tarde
df_accounts['account_created_date'] = pd.to_datetime(df_accounts['account_created_date'])
df_cases['case_created_date'] = pd.to_datetime(df_cases['case_created_date'])
df_cases['case_closed_date'] = pd.to_datetime(df_cases['case_closed_date'])

print(f"📊 Accounts carregados: {len(df_accounts)} registros")
print(f"📊 Cases carregados: {len(df_cases)} registros")

# %% [markdown]
# Análise Exploratória Detalhada

# %%
# Célula 3: Estrutura e Qualidade - Accounts
print("=" * 80)
print("ANÁLISE: ACCOUNTS")
print("=" * 80)

print("\n📋 Informações Gerais:")
print(df_accounts.info())

print("\n📊 Resumo Categórico (Top valores):")
cols_cat = ['account_country', 'account_industry']
display(df_accounts[cols_cat].describe())

print("\n📅 Resumo Temporal:")
print(f"Primeira conta criada em: {df_accounts['account_created_date'].min()}")
print(f"Última conta criada em:   {df_accounts['account_created_date'].max()}")
print(f"Período total de dados:   {df_accounts['account_created_date'].max() - df_accounts['account_created_date'].min()}")

print("\n🔍 Primeiras 5 linhas:")
display(df_accounts.head())

print("\n⚠️ Valores Nulos:")
print(df_accounts.isnull().sum())

print("\n🔑 Colunas disponíveis:")
print(df_accounts.columns.tolist())

# %%
# Célula 4: Estrutura e Qualidade - Cases
print("=" * 80)
print("ANÁLISE: SUPPORT CASES")
print("=" * 80)

print("\n📋 Informações Gerais:")
print(df_cases.info())

cols_negocio = ['case_status', 'case_priority', 'case_severity', 'case_product']

print("\n📊 Distribuição de Métricas Chave (Top 5):")
for col in cols_negocio:
    print(f"\n--- {col.upper()} ---")
    # Mostra contagem e % relativa lado a lado
    dist = pd.concat([df_cases[col].value_counts(), 
                      df_cases[col].value_counts(normalize=True).mul(100).round(1)], 
                     axis=1, keys=['Qtd', '%'])
    display(dist)

print("\n📅 Resumo Temporal dos Casos:")
print(f"Primeiro caso: {df_cases['case_created_date'].min()}")
print(f"Último caso:   {df_cases['case_created_date'].max()}")

print("\n⚠️ Valores Nulos (Importante para identificar casos abertos):")
print(df_cases.isnull().sum())

# %% [markdown]
# Identificação de Relacionamentos

# %%
# Célula 5: Verificação de Integridade (Abordagem Vetorizada)

# 1. Identificar IDs válidos (Conjunto de referência)
valid_account_ids = set(df_accounts['account_sfid'])

# 2. Criar a coluna de status com um valor padrão
df_cases['integrity_status'] = 'Valid Link'

# 3. Marcar os Nulos (Rápido e direto)
df_cases.loc[df_cases['account_sfid'].isnull(), 'integrity_status'] = 'Orphan (Null ID)'

# 4. Marcar os Links Quebrados (IDs que não são nulos, mas não estão na lista de contas)
# O operador ~ significa "NÃO". Ou seja: Onde o ID NÃO está em valid_account_ids
broken_link_mask = (~df_cases['account_sfid'].isin(valid_account_ids)) & (df_cases['account_sfid'].notnull())
df_cases.loc[broken_link_mask, 'integrity_status'] = 'Orphan (Broken Link)'

# === Relatório ===
print("=== Relatório de Integridade ===")
print(df_cases['integrity_status'].value_counts())

# Exibir amostra dos problemas, se houver
orphans = df_cases[df_cases['integrity_status'] != 'Valid Link']
if not orphans.empty:
    print(f"\nAlerta: Encontrados {len(orphans)} registros órfãos.")
    display(orphans[['case_number', 'account_sfid', 'integrity_status']].head())

# %%
# Célula 6: Tratamento dos Órfãos (Data Cleaning)

# Em vez de apagar, vamos preencher os Nulos para evitar erros no SQL depois
df_cases['account_sfid'] = df_cases['account_sfid'].fillna('UNKNOWN_ACCOUNT')

# Opcional: Se quiser ser muito proativo, crie uma conta "fictícia" no df_accounts
# para que o JOIN no SQL não descarte esses dados.
unknown_account = {
    'account_sfid': 'UNKNOWN_ACCOUNT',
    'account_name': 'Unassigned / Data Error',
    'account_industry': 'Unknown',
    'account_country': 'Unknown'
}

# Adiciona essa conta "coringa" ao DataFrame de contas se ela não existir
if 'UNKNOWN_ACCOUNT' not in df_accounts['account_sfid'].values:
    df_accounts = pd.concat([df_accounts, pd.DataFrame([unknown_account])], ignore_index=True)

print("Limpeza realizada: Órfãos mapeados para 'UNKNOWN_ACCOUNT'.")

# %% [markdown]
# Processamento com SQL 
# 
# Setup do Banco de Dados In-Memory

# %%
# Célula 7: Criação do Banco SQLite em Memória
conn = sqlite3.connect(':memory:')

# Carregando dados no SQLite
df_accounts.to_sql('accounts', conn, index=False, if_exists='replace')
df_cases.to_sql('cases', conn, index=False, if_exists='replace')

# Verificando tabelas criadas
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print("✅ Tabelas criadas no SQLite:")
print(tables)

# %% [markdown]
# Queries Analíticas (KPIs de Negócio)
# 
# KPI 1: Performance por Indústria

# %%
# Célula 8: Análise de Volume e Tempo por Indústria
query_industry = """
SELECT 
    a.account_industry as industry,
    COUNT(c.case_sfid) as total_cases,
    COUNT(DISTINCT c.account_sfid) as unique_accounts,
    -- SQLite usa JULIANDAY para diferença de datas
    ROUND(AVG(JULIANDAY(c.case_closed_date) - JULIANDAY(c.case_created_date)), 2) as avg_resolution_days,
    COUNT(CASE WHEN c.case_priority IN ('High', 'Urgent') THEN 1 END) as critical_priority_cases,
    ROUND(COUNT(CASE WHEN c.case_priority IN ('High', 'Urgent') THEN 1 END) * 100.0 / COUNT(c.case_sfid), 2) as pct_critical_cases
FROM 
    accounts a
JOIN 
    cases c ON a.account_sfid = c.account_sfid
WHERE 
    c.case_sfid IS NOT NULL
GROUP BY 
    a.account_industry
ORDER BY 
    total_cases DESC;
"""

# Usando nossa função auxiliar criada anteriormente (ou pd.read_sql)
df_industry_metrics = pd.read_sql(query_industry, conn)

print("📊 KPI 1: Métricas por Indústria")
display(df_industry_metrics)

# %% [markdown]
# KPI 2: Análise de Status de Cases

# %%
# Célula 9: Distribuição de Status
query_status = """
SELECT 
    c.case_status as status,
    COUNT(c.case_sfid) as total_cases,
    -- Tempo de resolução para casos FECHADOS
    ROUND(AVG(JULIANDAY(c.case_closed_date) - JULIANDAY(c.case_created_date)), 2) as avg_days_to_close,
    -- Contagem de Críticos (High + Urgent)
    COUNT(CASE WHEN c.case_priority IN ('High', 'Urgent') THEN 1 END) as critical_cases,
    -- Idade média (Backlog) para casos ABERTOS (considerando 'hoje' como 2025-01-09)
    ROUND(AVG(
        CASE 
            WHEN c.case_closed_date IS NULL 
            THEN JULIANDAY('2025-01-09') - JULIANDAY(c.case_created_date)
            ELSE NULL 
        END
    ), 2) as avg_days_open
FROM 
    cases c
GROUP BY 
    c.case_status
ORDER BY 
    total_cases DESC;
"""

df_status_metrics = pd.read_sql(query_status, conn)
print("📊 KPI 2: Análise por Status")
display(df_status_metrics)

# %% [markdown]
# KPI 3: Contas Problemáticas (High Touch Accounts)
# 

# %%
# Célula 10: Identificação de Contas com Muitos Cases (High Touch)
query_high_touch = """
SELECT 
    a.account_name,
    a.account_industry,
    COUNT(c.case_sfid) as total_cases,
    
    -- Métrica 1: Criticidade (Prioridade Alta + Urgente)
    COUNT(CASE WHEN c.case_priority IN ('High', 'Urgent') THEN 1 END) as critical_cases,
    
    -- Métrica 2: Backlog Atual (Casos que não estão Fechados nem são Duplicados)
    COUNT(CASE WHEN c.case_status NOT IN ('Closed', 'Duplicate') THEN 1 END) as active_cases,
    
    -- Métrica 3: % de Criticidade (Ajustado para incluir High e Urgent)
    ROUND(COUNT(CASE WHEN c.case_priority IN ('High', 'Urgent') THEN 1 END) * 100.0 / COUNT(c.case_sfid), 1) as pct_critical

FROM 
    accounts a
JOIN 
    cases c ON a.account_sfid = c.account_sfid
GROUP BY 
    a.account_sfid, a.account_name, a.account_industry
HAVING 
    total_cases > 10
ORDER BY 
    total_cases DESC
LIMIT 15
"""

df_high_touch = pd.read_sql(query_high_touch, conn)
print("📊 KPI 3: Top Clientes por Volume e Carga de Trabalho Atual")
display(df_high_touch)

# %% [markdown]
# KPI 4: Análise Temporal

# %%
# Célula 11: Tendências Temporais
query_temporal = """
SELECT 
    strftime('%Y-%m', c.case_created_date) as month,
    COUNT(c.case_sfid) as cases_created,
    COUNT(CASE WHEN c.case_status = 'Closed' THEN 1 END) as cases_closed,
    -- Cálculo de média de dias para resolução
    ROUND(AVG(JULIANDAY(c.case_closed_date) - JULIANDAY(c.case_created_date)), 2) as avg_resolution_days
FROM 
    cases c
WHERE
    c.case_created_date IS NOT NULL
GROUP BY 
    strftime('%Y-%m', c.case_created_date)
ORDER BY 
    month
"""

df_temporal = pd.read_sql(query_temporal, conn)
print("📊 KPI 4: Tendências Mensais")
display(df_temporal.tail(12)) # Mostrando apenas os últimos 12 meses para não poluir

# %% [markdown]
# Visualizações (Data Storytelling)
# 
# Visualização 1: Volume por Indústria

# %%
# Célula 12: Gráfico de Barras - Top Indústrias
import os

# 1. Garante que o diretório de saída existe (evita erro de FileNotFoundError)
os.makedirs('../output/figures', exist_ok=True)

plt.figure(figsize=(14, 8))

# Garante que pegamos apenas o top 10 ordenado
top_industries = df_industry_metrics.sort_values('total_cases', ascending=False).head(10)

# 2. Plotagem corrigida (adicionado hue e legend=False para evitar warnings recentes do Seaborn)
ax = sns.barplot(
    data=top_industries, 
    y='industry', 
    x='total_cases', 
    hue='industry',  # Boas práticas do Seaborn novo
    palette='viridis',
    legend=False
)

plt.title('Top 10 Indústrias por Volume de Casos de Suporte', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Número Total de Cases', fontsize=13)
plt.ylabel('Indústria', fontsize=13)

# 3. Adicionar valores nas barras (Ajuste de posição dinâmica)
for i, v in enumerate(top_industries['total_cases']):
    # O offset (+ v * 0.01) coloca o texto um pouco à frente da barra proporcionalmente
    ax.text(v + (v * 0.01), i, f'{v:,.0f}', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()

# Salva a figura
plt.savefig('../output/figures/01_volume_por_industria.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo em: ../output/figures/01_volume_por_industria.png")

plt.show()

# %% [markdown]
# Visualização 2: Tempo de Resolução

# %%
# Célula 13: Gráfico de Barras Horizontal - Tempo de Resolução (Corrigido Definitivo)
plt.figure(figsize=(14, 8))

# 1. FILTRO DE RELEVÂNCIA
df_relevante = df_industry_metrics[df_industry_metrics['total_cases'] > 20].copy()

# 2. CORREÇÃO DO ERRO VISUAL (TRATAMENTO DE NULOS)
# Substitui valores None/NaN por uma string para que o Seaborn consiga plotar a barra
df_relevante['industry'] = df_relevante['industry'].fillna('No Industry Defined')

# 3. Seleciona as 10 indústrias mais lentas
top_resolution = df_relevante.nlargest(10, 'avg_resolution_days')

# Plotagem
ax = sns.barplot(
    data=top_resolution, 
    y='industry', 
    x='avg_resolution_days', 
    hue='industry', 
    palette='rocket', 
    legend=False
)

plt.title('Top 10 Indústrias (Relevantes) com Maior Tempo Médio de Resolução', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Tempo Médio de Resolução (dias)', fontsize=13)
plt.ylabel('Indústria', fontsize=13)

# Adicionar valores nas barras
for i, v in enumerate(top_resolution['avg_resolution_days']):
    # Ajuste fino: Se o valor for muito pequeno, afasta um pouco mais
    offset = v * 0.01 if v > 1 else 0.1
    ax.text(v + offset, i, f'{v:.1f}d', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('../output/figures/02_tempo_resolucao.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo em: ../output/figures/02_tempo_resolucao_fixed.png")

plt.show()

# %% [markdown]
# Visualização 3: Distribuição de Status

# %%
# Célula 14: Gráfico de Pizza - Status dos Cases

plt.figure(figsize=(10, 6))

# Definição de cores
colors = sns.color_palette('pastel', len(df_status_metrics))
explode = [0.05 if i == 0 else 0 for i in range(len(df_status_metrics))]

# 1. Preparação dos Labels para a Legenda (Nome do Status + Porcentagem)
# Iteramos sobre o dataframe para criar textos como "Closed - 85.2%"
total = df_status_metrics['total_cases'].sum()
legend_labels = [f'{row.status} - {row.total_cases/total*100:.1f}%' 
                 for _, row in df_status_metrics.iterrows()]

# 2. Plotagem "Limpa" (Sem textos na pizza)
patches, texts = plt.pie(
    df_status_metrics['total_cases'], 
    labels=None,      # Remove labels das fatias
    autopct=None,     # Remove porcentagem das fatias
    colors=colors,
    explode=explode,
    startangle=90
)

# 3. Legenda Lateral Enriquecida
plt.legend(
    patches,
    legend_labels,    # Aqui entram os textos com porcentagem
    title="Status - Distribuição",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1) # Posição lateral segura
)

plt.title('Distribuição de Cases por Status', 
          fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('../output/figures/03_distribuicao_status.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo em: ../output/figures/03_distribuicao_status.png")

plt.show()

# %% [markdown]
# Visualização 4: Tendência Temporal

# %%
# Célula 15: Gráfico de Linha - Tendência Temporal

# Garante ordenação cronológica (essencial para gráficos de linha)
df_temporal = df_temporal.sort_values('month')

fig, ax1 = plt.subplots(figsize=(16, 8))

# --- Eixo Principal (Esquerda): Volume de Casos ---
color1 = 'tab:blue'
ax1.set_xlabel('Mês', fontsize=13)
ax1.set_ylabel('Número de Cases', color='#2c3e50', fontsize=13)

# Plot cases criados
ax1.plot(df_temporal['month'], df_temporal['cases_created'], 
         color='tab:blue', marker='o', linewidth=2, label='Cases Criados')

# Plot cases fechados
ax1.plot(df_temporal['month'], df_temporal['cases_closed'], 
         color='tab:green', marker='s', linewidth=2, label='Cases Fechados')

ax1.tick_params(axis='y', labelcolor='#2c3e50')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left')

# --- Eixo Secundário (Direita): Eficiência ---
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Tempo Médio de Resolução (dias)', color=color2, fontsize=13)

ax2.plot(df_temporal['month'], df_temporal['avg_resolution_days'], 
         color=color2, marker='^', linewidth=2, linestyle='--', label='Tempo Médio')

ax2.tick_params(axis='y', labelcolor=color2)
ax2.legend(loc='upper right') # Posição oposta para não sobrepor

# Títulos e Ajustes
plt.title('Evolução Temporal: Volume de Chamados vs Eficiência', 
          fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')

fig.tight_layout()
plt.savefig('../output/figures/04_tendencia_temporal.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo em: ../output/figures/04_tendencia_temporal.png")

plt.show()

# %% [markdown]
# Visualização 5: Matriz de Correlação 

# %%
# Célula 16: Heatmap - Prioridade vs Status
# 1. Carregar dados
priority_status = pd.read_sql("""
    SELECT 
        case_priority as priority,
        case_status as status,
        COUNT(*) as count
    FROM cases
    GROUP BY case_priority, case_status
""", conn)

# 2. Pivotagem
pivot_table = priority_status.pivot(index='priority', columns='status', values='count').fillna(0)

# 3. Ordenação Lógica (Do mais crítico para o menos crítico)
# Usamos a lista exata que você encontrou no banco
custom_order = ['Urgent', 'High', 'Normal', 'not_priority']

# Filtramos apenas o que realmente existe na tabela pivotada para evitar erros
existing_order = [p for p in custom_order if p in pivot_table.index]
pivot_table = pivot_table.reindex(existing_order)

# 4. Plotagem
plt.figure(figsize=(10, 6))
sns.heatmap(
    pivot_table, 
    annot=True, 
    fmt='g', 
    cmap='YlOrRd', # Vermelho para o que é Urgente
    linewidths=0.5,
    cbar_kws={'label': 'Volume de Casos'}
)

plt.title('Matriz de Calor: Volume de Casos por Prioridade', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Status Atual', fontsize=13)
plt.ylabel('Prioridade', fontsize=13)

plt.tight_layout()
plt.savefig('../output/figures/05_matriz_prioridade_status.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo em: ../output/figures/05_matriz_prioridade_status.png")

plt.show()

# %% [markdown]
# ## 💡 Insights de Negócio
# 
# ### 🎯 Insight 1: Risco de Concentração ("The Whale Client")
# 
# **Problema Identificado:**
# - **Cliente Outlier:** O cliente `Customer_900e52a5` (IT) representa **16.5%** de todos os casos.
# - **Volume:** 1.650 tickets (7x maior que o 2º colocado).
# - **Risco:** Backlog atual de 93 casos ativos, indicando potencial insatisfação/churn.
# 
# **Recomendação Estratégica:**
# - ✅ Implementar atendimento **White Glove** com Technical Account Manager (TAM) dedicado.
# - ✅ Investigar histórico de tickets para criar automação/self-service específico.
# - ✅ **Meta:** Reduzir volume de tickets deste cliente em 20% em 3 meses.
# 
# ---
# 
# ### 🎯 Insight 2: Ineficiência Operacional (Duplicatas e Priorização)
# 
# **Problema Identificado:**
# - **20.2% de Desperdício:** 2.015 casos são duplicatas, consumindo tempo precioso de triagem.
# - **Priorização Quebrada:** Apenas 2 casos "High" em todo histórico. A triagem é binária: "Normal" ou "Urgent".
# - **Gargalo:** Casos novos ("New") têm idade média de 159 dias no backlog.
# 
# **Recomendação Estratégica:**
# - ✅ Implementar validação de duplicidade no Front-End (UX).
# - ✅ Eliminar categoria "High" OU redefinir critérios claros de SLA.
# - ✅ **Meta:** Reduzir duplicatas para <5% e limpar o backlog antigo.
# 
# ---
# 
# ### 🎯 Insight 3: Dados Órfãos & Hegemonia Farmacêutica
# 
# **Problema Identificado:**
# - **Blind Spot:** **1.593 casos** (15.9%) sem vínculo com Account (orphan data).
# - **Impacto:** Impossibilita análise de receita e ROI do suporte ("voo às cegas").
# - **Setor Crítico:** Pharmaceuticals representa 7 das top 15 contas por volume.
# 
# **Recomendação Estratégica:**
# - ✅ **Curto Prazo:** Força-tarefa (ETL) para recuperar linkagem de casos órfãos.
# - ✅ **Médio Prazo:** Criar Squad Especializada em Life Sciences/Pharma.
# - ✅ **Meta:** Taxa de dados órfãos < 1% e aumentar CSAT do setor Pharma.


