from src.forecast import load_series

def test_load_series():
    df = load_series()
    assert "ds" in df.columns
    assert "y" in df.columns
    assert len(df) > 0
