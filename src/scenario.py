#!/usr/bin/env python3
"""scenario.py
What-if scenario engine. Accepts price shifts or promo changes and simulates demand and revenue.
Produces deterministic and Monte Carlo simulations.
"""
import argparse
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

DB_PATH = 'data/revenue.db'

def load_sales():
    conn = sqlite3.connect(DB_PATH)
    sales = pd.read_sql('SELECT * FROM sales', conn, parse_dates=['date'])
    conn.close()
    return sales

def apply_price_shift(sales, product_id, price_delta_pct):
    df = sales.copy()
    mask = df['product_id']==product_id
    df.loc[mask, 'price_new'] = df.loc[mask, 'price'] * (1 + price_delta_pct)
    # naive demand response using simple elasticity placeholder
    elasticity = -1.0  # default
    # estimate units change
    df.loc[mask, 'units_new'] = (df.loc[mask, 'units'] * (1 + elasticity * price_delta_pct)).clip(lower=0).round().astype(int)
    df.loc[mask, 'revenue_new'] = (df.loc[mask, 'price_new'] * df.loc[mask, 'units_new']).round(2)
    return df

def monte_carlo_price_sim(sales, product_id, price_delta_pct, n_sim=1000):
    results = []
    for i in range(n_sim):
        # sample elasticity from a distribution
        e = np.random.normal(-1.0, 0.3)
        df = sales.copy()
        mask = df['product_id']==product_id
        df.loc[mask, 'price_new'] = df.loc[mask, 'price'] * (1 + price_delta_pct)
        df.loc[mask, 'units_new'] = (df.loc[mask, 'units'] * (1 + e * price_delta_pct)).clip(lower=0)
        rev_new = (df.loc[mask, 'price_new'] * df.loc[mask, 'units_new']).sum()
        rev_old = (df.loc[mask, 'price'] * df.loc[mask, 'units']).sum()
        results.append({'sim': i, 'rev_old': rev_old, 'rev_new': rev_new})
    return pd.DataFrame(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--product-id', type=int, default=1)
    parser.add_argument('--price-delta-pct', type=float, default=0.05, help='Fractional change e.g. 0.05 for +5%')
    parser.add_argument('--output', default='outputs/scenario_results.xlsx')
    args = parser.parse_args()
    sales = load_sales()
    det = apply_price_shift(sales, args.product_id, args.price_delta_pct)
    mc = monte_carlo_price_sim(sales, args.product_id, args.price_delta_pct, n_sim=500)
    Path('outputs').mkdir(exist_ok=True)
    # save deterministic summary and MC results
    det_summary = det[det['product_id']==args.product_id][['date','product_id','units','price','units_new','price_new','revenue','revenue_new']]
    with pd.ExcelWriter(args.output) as writer:
        det_summary.to_excel(writer, sheet_name='deterministic', index=False)
        mc.to_excel(writer, sheet_name='monte_carlo', index=False)
    print(f'Wrote scenario results to {args.output}')
