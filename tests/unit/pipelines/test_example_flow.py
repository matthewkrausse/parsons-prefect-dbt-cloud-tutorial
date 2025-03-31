import pytest
import pandas as pd
from datetime import datetime
from pipelines.flows.example_flow import extract_data, transform_data

def test_extract_data():
    """Test that extract_data returns a dataframe with expected structure."""
    result = extract_data()
    
    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert "value" in result.columns
    assert "timestamp" in result.columns
    assert len(result) == 10

def test_transform_data():
    """Test that transform_data correctly transforms the input data."""
    # Create test input data
    input_data = pd.DataFrame({
        "id": [1, 2, 3],
        "value": [10, 20, 30],
        "timestamp": [datetime.now() for _ in range(3)]
    })
    
    result = transform_data(input_data)
    
    # Verify transformation was applied
    assert "calculated_value" in result.columns
    assert result["calculated_value"].tolist() == [20, 40, 60]
