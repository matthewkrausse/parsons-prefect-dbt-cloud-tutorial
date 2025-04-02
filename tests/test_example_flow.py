import pytest
from unittest.mock import patch, MagicMock
from parsons import Table

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
        {"name": "John Smith", "party": "Democrat", "age": 42},
        {"name": "Sarah Johnson", "party": "Republican", "age": 35},
        {"name": "Miguel Rodriguez", "party": "Independent", "age": 29},
    ]

    return Table(data)


def test_extract_data_with_parsons():
    """Test that extract_data_with_parsons creates a table with expected structure."""
    result = extract_data_with_parsons()

    assert isinstance(result, Table)
    assert result.num_rows == 3
    assert set(result.columns) == {"name", "party", "age"}
    assert all(isinstance(row["age"], int) for row in result)
    assert all(isinstance(row["name"], str) for row in result)


def test_transform_data(sample_parsons_table):
    """Test that transform_data modifies the table as expected."""
    result = transform_data(sample_parsons_table)

    assert isinstance(result, Table)
    assert result.num_rows == 3
    assert "name_upper" in result.columns
    assert all(isinstance(row["name_upper"], str) for row in result)
    assert all(row["name_upper"] == row["name"].upper() for row in result)


@patch("pipelines.flows.example_flow.GoogleBigQuery")
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
    assert "dev_parsons_test.parsons_test" in kwargs.get("table_name", "")
    assert kwargs.get("if_exists") == "drop"


@patch("pipelines.flows.example_flow.GoogleBigQuery")
@patch("pipelines.flows.example_flow.get_secret")
def test_load_data_with_parsons_prod(
    mock_get_secret, mock_bigquery, sample_parsons_table
):
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


@patch("pipelines.flows.example_flow.load_data_with_parsons")
@patch("pipelines.flows.example_flow.transform_data")
@patch("pipelines.flows.example_flow.extract_data_with_parsons")
def test_example_pipeline_default_env(
    mock_extract, mock_transform, mock_load, sample_parsons_table
):
    """Test the main pipeline flow with default environment."""
    mock_extract.return_value = sample_parsons_table
    mock_transform.return_value = sample_parsons_table

    example_pipeline()

    mock_extract.assert_called_once()
    mock_transform.assert_called_once_with(sample_parsons_table)
    mock_load.assert_called_once_with(sample_parsons_table, "dev")


@patch("pipelines.flows.example_flow.load_data_with_parsons")
@patch("pipelines.flows.example_flow.transform_data")
@patch("pipelines.flows.example_flow.extract_data_with_parsons")
def test_example_pipeline_prod_env(
    mock_extract, mock_transform, mock_load, sample_parsons_table
):
    """Test the main pipeline flow with production environment."""
    mock_extract.return_value = sample_parsons_table
    mock_transform.return_value = sample_parsons_table

    example_pipeline("prod")

    mock_extract.assert_called_once()
    mock_transform.assert_called_once_with(sample_parsons_table)
    mock_load.assert_called_once_with(sample_parsons_table, "prod")
