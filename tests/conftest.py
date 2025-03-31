import pytest
import os
import sys

# Add project root to path so pytest can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define fixtures that can be used across tests
@pytest.fixture
def sample_dataframe():
    """Fixture that returns a sample dataframe for testing."""
    import pandas as pd
    from datetime import datetime
    
    return pd.DataFrame({
        "id": [1, 2, 3],
        "value": [10, 20, 30],
        "timestamp": [datetime.now() for _ in range(3)]
    })
