#!/usr/bin/env python3
"""forecast.py
Forecasting pipeline skeleton. Supports Prophet and SARIMAX (statsmodels).
This file includes training and evaluation functions and example usage.
"""
import argparse
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

DB_PATH = Path('data/revenue.db')

def load_series(product_id=None):
    conn = sqlite3.connect(DB_PATH)
    q = 'SELECT date, product_id, SUM(revenue) as revenue FROM sales GROUP BY date, product_id'
    df = pd.read_sql(q, conn, parse_dates=['date'])
    conn.close()
    if product_id:
        df = df[df.product_id==product_id].copy()
    # aggregate daily revenue
    agg = df.groupby('date')['revenue'].sum().reset_index()
    agg = agg.rename(columns={'date':'ds','revenue':'y'})
    return agg

def train_prophet(df):
    try:
        from prophet import Prophet
    except Exception as e:
        raise RuntimeError('prophet library not available. Install via `pip install prophet`') from e
    m = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=True)
    m.fit(df)
    future = m.make_future_dataframe(periods=90)
    forecast = m.predict(future)
    return forecast

def train_sarimax(df):
    import statsmodels.api as sm
    # simplistic: remove NaNs and index
    ts = df.set_index('ds')['y'].asfreq('D').fillna(method='ffill')
    # fit ARIMA(1,1,1) for example
    model = sm.tsa.SARIMAX(ts, order=(1,1,1), seasonal_order=(0,1,1,7))
    res = model.fit(disp=False)
    pred = res.get_prediction(start=ts.index[0], end=ts.index[-1] + pd.Timedelta(days=90))
    forecast = pred.predicted_mean.reset_index().rename(columns={'index':'ds', 0:'yhat'})
    return forecast

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-path', default=str(DB_PATH))
    parser.add_argument('--method', choices=['prophet','sarimax'], default='prophet')
    args = parser.parse_args()
    df = load_series()
    if args.method == 'prophet':
        print('Training Prophet (requires prophet package)...')
        try:
            f = train_prophet(df)
            print(f.tail()[['ds','yhat','yhat_lower','yhat_upper']])
        except Exception as e:
            print('Prophet training failed:', e)
    else:
        print('Training SARIMAX (statsmodels)...')
        try:
            f = train_sarimax(df)
            print(f.tail())
        except Exception as e:
            print('SARIMAX training failed:', e)
