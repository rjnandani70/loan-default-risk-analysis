LOAN DEFAULT RISK ANALYSIS (Portfolio Project)

Project Goal
- Analyze loan performance data to estimate default risk.
- Build analyst-ready outputs for SQL validation, Power BI dashboarding, and Excel quality checks.

Tech Stack
- Python: pandas, numpy, scikit-learn
- SQL: PostgreSQL-compatible scripts
- Power BI: dashboard over processed outputs
- Excel: data quality checks and pivot analysis

Repository Structure
- data/raw: generated source loan data
- data/processed: cleaned features, KPIs, and scored outputs
- src: Python pipeline scripts
- sql: schema and KPI queries
- powerbi: dashboard instructions and DAX starter measures
- excel: QA and pivot checklist
- reports: project summary and business recommendations

Run Instructions
1) Create environment and install packages:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2) Run full pipeline:
   python3 src/generate_data.py
   python3 src/preprocess.py
   python3 src/analysis_and_model.py