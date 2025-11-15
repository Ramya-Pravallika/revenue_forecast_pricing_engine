import pandas as pd
from src.elasticity import estimate_elasticity

def test_elasticity_output():
    sample = pd.DataFrame({
        "product_id": [1,1],
        "cohort": ["active", "active"],
        "units": [10, 12],
        "price": [20, 22],
        "promo_id": [None, None],
        "date": pd.to_datetime(["2020-01-01","2020-01-02"])
    })
    result = estimate_elasticity(sample)
    assert "elasticity" in result.columns
