from src.scenario import apply_price_shift
import pandas as pd

def test_apply_price_shift():
    sample = pd.DataFrame({
        "product_id": [1],
        "units": [10],
        "price": [100],
        "revenue": [1000],
        "date": pd.to_datetime(["2020-01-01"])
    })
    out = apply_price_shift(sample, 1, 0.1)
    assert "price_new" in out.columns
    assert "units_new" in out.columns
