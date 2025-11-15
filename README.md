# Revenue Forecasting & Pricing Insights Engine

**Languages / Tools**: Python (Prophet / ARIMA), SQL (SQLite), Excel, Power BI, Statistics

**What this repository contains**  
This repository is a complete, runnable scaffold for a revenue forecasting + pricing insights engine. It contains:
- `data/` — synthetic sample data (sales history, products, promotions, market indicators).
- `sql/` — example SQL schema and queries (SQLite).
- `src/` — Python modules:
  - `etl.py` — feature assembly and DB loader
  - `forecast.py` — forecasting pipeline (Prophet / ARIMA placeholders)
  - `elasticity.py` — pricing elasticity estimation and diagnostics
  - `scenario.py` — what-if engine and Monte Carlo simulation
  - `utils.py` — helper utilities
- `notebooks/` — a Jupyter notebook walkthrough (`walkthrough.ipynb`) that demonstrates the end-to-end flow with the synthetic data.
- `outputs/` — example Excel outputs and CSVs created by the pipeline.
- `requirements.txt` — Python package list.
- `README.md` — this file.

---

## Project Problem
Retail businesses and subscription services need accurate revenue forecasts and pricing recommendations to maximize margin without harming conversion. This project does:
1. Build demand and revenue forecasts that combine historical sales, seasonality, promotions, and external market indicators.
2. Estimate cohort-level price elasticities to identify pricing bands.
3. Provide a scenario engine to simulate promotional and price-change impacts on revenue & margin.
4. Deliver outputs suitable for business consumption (Excel + Power BI).

---

## How to use this repo (quickstart)
1. Clone or download this repository.
2. Create a Python environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
3. Run the synthetic data generator and ETL to populate a local SQLite:
```bash
python src/etl.py --generate-synthetic
```
4. Run the forecast pipeline (note: Prophet must be installed; alternatives supported):
```bash
python src/forecast.py --db-path data/revenue.db --method prophet
```
5. Estimate price elasticity:
```bash
python src/elasticity.py --db-path data/revenue.db
```
6. Run scenario simulations and export Excel results:
```bash
python src/scenario.py --db-path data/revenue.db --output outputs/scenario_results.xlsx
```
7. Open `notebooks/walkthrough.ipynb` for a guided notebook exploring results, charts, and how to push data to Power BI.

---

## What I built
- Reproducible pipeline that assembles features with SQL/Pandas and writes to a SQLite DB.
- Forecasting module supporting Prophet and SARIMAX (code + training/evaluation functions).
- Elasticity module using cohort-level regressions with diagnostic outputs and a simple instrumental-variable placeholder.
- Scenario engine implementing deterministic and Monte Carlo simulations to produce revenue & margin distributions.
- Excel export that can be opened by analysts and used as a source for Power BI.
- A clear README and Jupyter notebook demonstrating end-to-end usage.

---

## Files and short descriptions
- requirements.txt

---
## Sample output and the Dashboard

<img width="641" height="463" alt="image" src="https://github.com/user-attachments/assets/756b4966-15f7-4294-907c-c496bad5cb9e" />
<img width="838" height="541" alt="image" src="https://github.com/user-attachments/assets/11fe53d1-ca1a-47a8-a533-da294edfe7d1" />
