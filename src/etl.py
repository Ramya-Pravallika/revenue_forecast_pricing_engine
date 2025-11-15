#!/usr/bin/env python3
"""etl.py
Generate synthetic data, assemble features and save to SQLite database.
"""
import argparse, sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path('data/revenue.db')

def generate_synthetic_data(start_date='2020-01-01', days=1095, n_products=10, n_customers=500):
    # dates
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    # products
    products = pd.DataFrame({
        'product_id': range(1, n_products+1),
        'sku': [f'SKU-{i:03d}' for i in range(1, n_products+1)],
        'category': ['A' if i%2==0 else 'B' for i in range(n_products)],
        'base_cost': np.round(np.random.uniform(5, 50, size=n_products),2)
    })
    # customers
    cohorts = ['new','active','churn-risk']
    customers = pd.DataFrame({
        'customer_id': range(1, n_customers+1),
        'cohort': np.random.choice(cohorts, size=n_customers, p=[0.2,0.7,0.1])
    })
    # promotions
    promos = pd.DataFrame([
        (1,'NewYear', '2020-01-05','2020-01-15', 0.1),
        (2,'SummerSale', '2020-06-10','2020-06-25', 0.2),
        (3,'BlackFri', '2020-11-20','2020-11-30', 0.25),
    ], columns=['promo_id','promo_name','start_date','end_date','discount_pct'])
    promos['start_date'] = pd.to_datetime(promos['start_date'])
    promos['end_date'] = pd.to_datetime(promos['end_date'])

    # market indicators
    mi = pd.DataFrame({
        'date': dates,
        'indicator_gdp': np.sin(np.arange(len(dates))/365*2*np.pi)*0.5 + 2 + np.random.normal(0,0.1,len(dates)),
        'indicator_sentiment': np.random.normal(0.5, 0.05, len(dates))
    })

    # sales generation
    sales = []
    sale_id = 1
    for d in dates:
        for pid in products['product_id']:
            base_demand = 20 + pid*2 + 5*np.sin((d.dayofyear/365)*2*np.pi)
            # promo?
            promo_id = None
            discount = 0.0
            for _,r in promos.iterrows():
                if r['start_date'] <= d <= r['end_date']:
                    promo_id = int(r['promo_id'])
                    discount = float(r['discount_pct'])
            # price varying by product and small noise
            price = round(products.loc[products.product_id==pid, 'base_cost'].values[0] * (1.5 + np.random.normal(0,0.05)),2)
            price = price * (1 - discount)
            units = max(0, int(np.random.poisson(base_demand*(1 - discount*2))))
            revenue = round(units * price,2)
            # choose a random customer
            cust = np.random.randint(1, customers.shape[0]+1)
            sales.append((sale_id, d.strftime('%Y-%m-%d'), pid, int(cust), int(units), float(price), float(revenue), promo_id))
            sale_id += 1

    sales_df = pd.DataFrame(sales, columns=['sale_id','date','product_id','customer_id','units','price','revenue','promo_id'])

    # write to sqlite
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    products.to_sql('products', conn, if_exists='replace', index=False)
    customers.to_sql('customers', conn, if_exists='replace', index=False)
    promos.to_sql('promotions', conn, if_exists='replace', index=False)
    mi.to_sql('market_indicators', conn, if_exists='replace', index=False)
    sales_df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Wrote synthetic DB to {DB_PATH}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-synthetic', action='store_true', help='Generate synthetic data and load to data/revenue.db')
    args = parser.parse_args()
    if args.generate_synthetic:
        generate_synthetic_data()
    else:
        print('Run with --generate-synthetic to create sample data.')
