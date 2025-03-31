import os
import pytest
from unittest.mock import MagicMock, patch
from pipelines.flows.utilities import get_secret

@pytest.fixture
def mock_secretmanager():
    """Fixture to mock Google Secret Manager client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.payload.data.decode.return_value = "secret_from_gsm"
    mock_client.access_secret_version.return_value = mock_response
    
    with patch('google.cloud.secretmanager.SecretManagerServiceClient', return_value=mock_client):
        yield mock_client, mock_response


def test_get_secret_from_env(monkeypatch):
    """Test retrieving secret from environment variables."""
    secret_id = "test_secret"
    secret_value = "test_value"
    
    # Setup environment variable
    monkeypatch.setenv(secret_id.upper(), secret_value)
    
    # Call the function
    result = get_secret(secret_id=secret_id)
    
    # Assert the result
    assert result == secret_value


def test_get_secret_from_secret_manager(monkeypatch, mock_secretmanager):
    """Test retrieving secret from Google Secret Manager when not in environment."""
    mock_client, _ = mock_secretmanager
    
    # Mock the environment to not have the variable
    monkeypatch.delenv("TEST_SECRET", raising=False)
    
    result = get_secret(project_id="test-project", secret_id="test_secret")
    
    # Assert the result
    assert result == "secret_from_gsm"
    
    # Verify the client was called with correct parameters
    mock_client.access_secret_version.assert_called_once_with(
        request={"name": "projects/test-project/secrets/test_secret/versions/latest"}
    )


def test_get_secret_with_custom_version(monkeypatch, mock_secretmanager):
    """Test retrieving secret with a specific version."""
    mock_client, _ = mock_secretmanager
    
    # Mock the environment to not have the variable
    monkeypatch.delenv("TEST_SECRET", raising=False)
    
    result = get_secret(project_id="test-project", secret_id="test_secret", version_id="2")
    
    # Assert the result
    assert result == "secret_from_gsm"
    
    # Verify the client was called with correct parameters
    mock_client.access_secret_version.assert_called_once_with(
        request={"name": "projects/test-project/secrets/test_secret/versions/2"}
    )


def test_get_secret_dotenv_loading():
    """Test that dotenv.load_dotenv is called."""
    with patch('dotenv.load_dotenv') as mock_load_dotenv:
        # Setup environment variable
        with patch.dict(os.environ, {"TEST_SECRET": "env_value"}):
            result = get_secret(secret_id="test_secret")
            
            # Verify dotenv.load_dotenv was called
            mock_load_dotenv.assert_called_once()
            
            # Assert the result
            assert result == "env_value"


def test_get_secret_none_secret_id():
    """Test that attempting to use None as secret_id raises an AttributeError."""
    with pytest.raises(AttributeError):
        get_secret(secret_id=None)


def test_get_secret_exception_propagation(monkeypatch):
    """Test that exceptions from Secret Manager are propagated."""
    # Mock the environment to not have the variable
    monkeypatch.delenv("TEST_SECRET", raising=False)
    
    # Mock the Secret Manager client to raise an exception
    mock_client = MagicMock()
    mock_client.access_secret_version.side_effect = Exception("Error accessing secret")
    
    # Patch the Secret Manager client class
    with patch('google.cloud.secretmanager.SecretManagerServiceClient', return_value=mock_client):
        with pytest.raises(Exception):
            get_secret(project_id="test-project", secret_id="test_secret")