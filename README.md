> 🇧🇷 [Leia este documento em Português](README.pt-br.md)

# GlobalVision Systems & Data Intern - Take Home Challenge

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 About the Project

This project presents a comprehensive analysis of **Accounts** and **Support Cases** data extracted from GlobalVision's Salesforce. The goal is to process, transform, and visualize data to generate actionable insights that support strategic business decisions.

---

## 🎯 Challenge Objectives

1.  **Data Exploration**: Understand the structure and quality of the datasets.
2.  **SQL Processing**: Use SQL within Python for transformations and aggregations.
3.  **Visualizations**: Create charts that communicate insights clearly.
4.  **Business Intelligence**: Propose recommendations based on quantitative evidence.

---

## 📂 Project Structure

```
globalvision-data-analysis/
│
├── data/
│   └── raw/
│       ├── accounts_anonymized.json
│       └── support_cases_anonymized.json
│
├── notebooks/
│   ├── analysis_walkthrough.ipynb # Main Notebook (Interactive Analysis)
│   └── analysis_walkthrough.py    # Python Script (Executable Version)
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

## 🚀 How to Run

### Prerequisites

- Python 3.8 or higher

### Installation

1.  **Clone the repository** (or extract the project files)

```bash
cd globalvision-data-analysis
```

2.  **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3.  **Install dependencies**

```bash
pip install -r requirements.txt
```

### Running the Analysis

**Option 1: Jupyter Notebook (Recommended)**

```bash
jupyter notebook notebooks/analysis_walkthrough.ipynb
```

Execute all cells sequentially (Menu: Cell > Run All).

**Option 2: Python Script**

If you prefer to run it as a Python script:

```bash
python notebooks/analysis_walkthrough.py
```

---

## 📊 Datasets Used

### 1. `accounts_anonymized.json`
-   **Records**: 1,415 accounts
-   **Period**: Nov/2007 - Jan/2025
-   **Key Fields**: `account_sfid`, `account_name`, `account_industry`, `account_country`

### 2. `support_cases_anonymized.json`
-   **Records**: 10,000 support cases
-   **Period**: Nov/2023 - Jan/2025
-   **Key Fields**: `case_sfid`, `account_sfid`, `case_status`, `case_priority`, `case_severity`

---

## 🔍 Developed KPIs

### KPI 1: Industry Performance
-   Total case volume by sector
-   Average resolution time (MTTR)
-   Percentage of critical cases (High + Urgent)

### KPI 2: Status Analysis
-   Case distribution by status (Closed, New, Working, etc.)
-   Current backlog (open cases)
-   Resolution efficiency

### KPI 3: High-Touch Accounts
-   Identification of accounts with high ticket volume
-   Criticality analysis by client
-   VIP service prioritization

### KPI 4: Temporal Trends
-   Monthly evolution of created vs. closed cases
-   Variation in average resolution time
-   Seasonality and demand patterns

---

## 📈 Key Visualizations

| Chart | Description | Key Insight |
| :--- | :--- | :--- |
| **Volume by Industry** | Horizontal bars showing top 10 sectors | Pharmaceuticals and IT dominate 45% of cases |
| **Resolution Time** | Efficiency comparison between industries | "None" sector has a 23-day MTTR (outlier) |
| **Status Distribution** | Pie chart with Closed/Open/Duplicate % | 70.4% closure rate |
| **Temporal Trend** | Double line chart (Volume + Efficiency) | Inflow volume exceeds outflow (Growing Backlog) |
| **Priority Matrix** | Priority vs. Status Heatmap | "High" category is almost never used |

---

## 💡 Business Insights

### 🎯 Insight 1: Concentration Risk ("The Whale Client")

**Identified Problem:**
-   **Outlier Client:** Client `Customer_900e52a5` (IT) represents **16.5%** of all cases.
-   **Volume:** 1,650 tickets (7x higher than the 2nd place).
-   **Risk:** Current backlog of 93 active cases, indicating potential dissatisfaction/churn.

**Strategic Recommendation:**
-   ✅ Implement **White Glove** service with a dedicated Technical Account Manager (TAM).
-   ✅ Investigate ticket history to create specific automation/self-service.
-   ✅ **Goal:** Reduce ticket volume from this client by 20% in 3 months.

---

### 🎯 Insight 2: Operational Inefficiency (Duplicates and Prioritization)

**Identified Problem:**
-   **20.2% Waste:** 2,015 cases are duplicates, consuming precious triage time.
-   **Broken Prioritization:** Only 2 "High" cases in the entire history. Triage is binary: "Normal" or "Urgent".
-   **Bottleneck:** New cases ("New") have an average age of 159 days in the backlog.

**Strategic Recommendation:**
-   ✅ Implement duplicate validation on the Front-End (UX).
-   ✅ Eliminate the "High" category OR redefine clear SLA criteria.
-   ✅ **Goal:** Reduce duplicates to <5% and clear the old backlog.

---

### 🎯 Insight 3: Orphan Data & Pharmaceutical Dominance

**Identified Problem:**
-   **Blind Spot:** **1,593 cases** (15.9%) have no link to an Account (orphan data).
-   **Impact:** Impossible to analyze revenue and ROI for support ("flying blind").
-   **Critical Sector:** Pharmaceuticals represents 7 of the top 15 accounts by volume.

**Strategic Recommendation:**
-   ✅ **Short Term:** Task Force (ETL) to recover orphan case linkage.
-   ✅ **Medium Term:** Create a Specialized Squad for Life Sciences/Pharma.
-   ✅ **Goal:** Orphan data rate < 1% and increase CSAT for the Pharma sector.

---

## 🛠️ Technologies Used

-   **Python 3.8+**: Main language
-   **Pandas**: Data manipulation and analysis
-   **SQLite3**: In-memory database for SQL queries
-   **Matplotlib & Seaborn**: Static visualizations
-   **NumPy**: Numerical operations
-   **Jupyter Notebook**: Interactive development environment

---

## 📦 Dependencies (requirements.txt)

```txt
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
numpy>=1.24.0
jupyter>=1.0.0
```

---

## 👤 Author

**Alex Oliveira Mendes**

📧 Email: [Alex_vips2@hotmail.com]
💼 LinkedIn: [https://www.linkedin.com/in/alex-mendes-80244b292]

---

## 📝 Development Notes

### Challenges Faced
1.  **Data Integrity**: 15.9% of cases without a valid `account_sfid`.
2.  **Data Quality**: "High" category practically unused.
3.  **Outliers**: A single client representing 16% of total volume.

### Technical Decisions
-   Creation of an "UNKNOWN_ACCOUNT" to preserve orphan cases in the analysis.
-   Use of in-memory SQLite to demonstrate SQL proficiency without external setup.
-   Focus on exportable visualizations (300dpi PNG) for executive presentations.

---

## 🎓 Key Takeaways

-   JSON data processing at scale.
-   Complex SQL queries with aggregations and JOINs.
-   Data storytelling through visualizations.
-   Translating technical insights into business recommendations.

---

## 📄 License

This project was developed as part of a selection process for GlobalVision.
Code available under MIT license for educational purposes.

---

## 🙏 Acknowledgments

I would like to thank the GlobalVision team for the opportunity to demonstrate my technical and analytical skills through this stimulating challenge!

---

**Submission Date**: January 2026
**Development Time**: 1 week
**Status**: ✅ Complete and Ready for Presentation