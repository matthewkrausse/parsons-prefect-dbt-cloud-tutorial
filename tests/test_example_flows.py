import pytest
from unittest.mock import patch, MagicMock
from parsons import Table
from datetime import datetime

from pipelines.flows.example_flow import (
    example_pipeline,
    extract_data_with_parsons,
    transform_data,
    load_data_with_parsons,
)


@pytest.fixture
def sample_parsons_table():
    """Create a sample Parsons Table for testing."""
    data = [
        {
            "id": i,
            "value": i * 10,
            "timestamp": datetime.now().isoformat()
        }
        for i in range(1, 11)
    ]
    return Table(data)


def test_extract_data_with_parsons():
    """Test that extract_data_with_parsons creates a table with expected structure."""
    result = extract_data_with_parsons()
    
    assert isinstance(result, Table)
    assert result.num_rows == 10
    assert set(result.columns) == {"id", "value", "timestamp"}
    assert all(isinstance(row["id"], int) for row in result)
    assert all(isinstance(row["value"], int) for row in result)


def test_transform_data(sample_parsons_table):
    """Test that transform_data correctly transforms the data."""
    result = transform_data(sample_parsons_table)
    
    assert "calculated_value" in result.columns
    assert all(row["calculated_value"] == row["value"] * 2 for row in result)
    assert result.num_rows == sample_parsons_table.num_rows


@patch('pipelines.flows.example_flow.GoogleBigQuery')
def test_load_data_with_parsons_dev(mock_bigquery, sample_parsons_table):
    """Test loading data in dev environment."""
    mock_bq_instance = MagicMock()
    mock_bigquery.return_value = mock_bq_instance
    mock_bq_instance.client.create_dataset = MagicMock()
    mock_bq_instance.copy = MagicMock()
    
    load_data_with_parsons(sample_parsons_table, "dev")
    
    # Verify dataset creation with dev prefix
    mock_bq_instance.client.create_dataset.assert_called_once_with(
        dataset="dev_parsons_test", exists_ok=True
    )
    
    # Verify copy was called with correct parameters
    mock_bq_instance.copy.assert_called_once()
    args, kwargs = mock_bq_instance.copy.call_args
    assert args[0] == sample_parsons_table  # First arg should be the table
    assert "dev_parsons_test.parsons_test" in kwargs.get('table_name', '')
    assert kwargs.get('if_exists') == "drop"


@patch('pipelines.flows.example_flow.GoogleBigQuery')
@patch('pipelines.flows.example_flow.get_secret')
def test_load_data_with_parsons_prod(mock_get_secret, mock_bigquery, sample_parsons_table):
    """Test loading data in prod environment."""
    mock_get_secret.return_value = '{"type": "service_account"}'
    mock_bq_instance = MagicMock()
    mock_bigquery.return_value = mock_bq_instance
    
    load_data_with_parsons(sample_parsons_table, "prod")
    
    # Verify get_secret was called
    mock_get_secret.assert_called_once_with("gcp_service_account")
    
    # Verify dataset creation without dev prefix
    mock_bq_instance.client.create_dataset.assert_called_once_with(
        dataset="parsons_test", exists_ok=True
    )


@patch('pipelines.flows.example_flow.load_data_with_parsons')
@patch('pipelines.flows.example_flow.transform_data')
@patch('pipelines.flows.example_flow.extract_data_with_parsons')
def test_example_pipeline_default_env(mock_extract, mock_transform, mock_load, sample_parsons_table):
    """Test the main pipeline flow with default environment."""
    mock_extract.return_value = sample_parsons_table
    mock_transform.return_value = sample_parsons_table
    
    example_pipeline()
    
    mock_extract.assert_called_once()
    mock_transform.assert_called_once_with(sample_parsons_table)
    mock_load.assert_called_once_with(sample_parsons_table, "dev")


@patch('pipelines.flows.example_flow.load_data_with_parsons')
@patch('pipelines.flows.example_flow.transform_data')
@patch('pipelines.flows.example_flow.extract_data_with_parsons')
def test_example_pipeline_prod_env(mock_extract, mock_transform, mock_load, sample_parsons_table):
    """Test the main pipeline flow with production environment."""
    mock_extract.return_value = sample_parsons_table
    mock_transform.return_value = sample_parsons_table
    
    example_pipeline("prod")
    
    mock_extract.assert_called_once()
    mock_transform.assert_called_once_with(sample_parsons_table)
    mock_load.assert_called_once_with(sample_parsons_table, "prod")