#!/usr/bin/env python3
"""elasticity.py
Estimate price elasticity by cohort and product using OLS regressions with basic controls.
Outputs a CSV with elasticity estimates and diagnostic columns.
"""
import argparse
import sqlite3
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from pathlib import Path

DB_PATH = 'data/revenue.db'

def load_data():
    conn = sqlite3.connect(DB_PATH)
    sales = pd.read_sql('SELECT s.*, c.cohort FROM sales s LEFT JOIN customers c ON s.customer_id=c.customer_id', conn, parse_dates=['date'])
    conn.close()
    return sales

def estimate_elasticity(df):
    # Add log transformations and group keys
    df = df.copy()
    df['log_units'] = (df['units']+1).apply(lambda x: np.log(x))
    df['log_price'] = df['price'].apply(lambda x: np.log(x+1e-9))
    results = []
    for (product_id, cohort), grp in df.groupby(['product_id','cohort']):
        try:
            # simple OLS: log(units) ~ log(price) + C(promo_id) + date dummies (month)
            grp['month'] = grp['date'].dt.month
            mdl = smf.ols('log_units ~ log_price + C(promo_id) + C(month)', data=grp).fit()
            elasticity = mdl.params.get('log_price', float('nan'))
            se = mdl.bse.get('log_price', float('nan'))
            results.append({
                'product_id': product_id,
                'cohort': cohort,
                'elasticity': float(elasticity),
                'se': float(se),
                'n_obs': int(grp.shape[0])
            })
        except Exception as e:
            results.append({
                'product_id': product_id,
                'cohort': cohort,
                'elasticity': None,
                'se': None,
                'n_obs': int(grp.shape[0])
            })
    return pd.DataFrame(results)

if __name__ == '__main__':
    df = load_data()
    res = estimate_elasticity(df)
    Path('outputs').mkdir(exist_ok=True)
    res.to_csv('outputs/elasticity_estimates.csv', index=False)
    print('Wrote outputs/elasticity_estimates.csv')
