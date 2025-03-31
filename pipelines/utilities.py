"""
Utility functions for prefect flows.
"""

import os
import subprocess
from google.cloud import secretmanager
import dotenv


def determine_git_environment():
    """
    Determine environment based on multiple signals.
    Returns 'prod' for main branch, 'dev' otherwise.
    """
    # 1. Check for explicit environment variable
    env_var = os.environ.get("ENVIRONMENT")
    if env_var:
        print(f"Using environment from ENVIRONMENT variable: {env_var}")
        return env_var.lower()

    # 2. Check for GitHub Actions environment
    if os.environ.get("GITHUB_REF") == "refs/heads/main":
        print("Detected GitHub main branch, using prod environment")
        return "prod"

    # 3. Try git branch as fallback for local development
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
        branch = result.stdout.strip()
        print(f"Git branch detected: {branch}")

        if branch == "main":
            return "prod"
        else:
            return "dev"
    except Exception as e:
        print(f"Git detection failed: {e}")

    # 4. Default fallback
    print("Using default environment: dev")
    return "dev"


def get_secret(project_id="your-gcp-project-id", secret_id=None, version_id="latest"):
    """
    Access the secret value, first checking environment variables,
    then falling back to Google Secret Manager.

    Args:
        project_id: Google Cloud project ID
        secret_id: Name of the secret (For local env, use UPPERCASE in the .env file)
        version_id: Secret version, defaults to "latest"

    Returns:
        The secret value as a string
    """
    # Load environment variables from .env file
    dotenv.load_dotenv()

    # First check if the secret exists as an environment variable
    env_value = os.environ.get(secret_id.upper())
    if env_value:
        print(f"Using {secret_id} from environment variables")
        return env_value

    print(
        f"Secret {secret_id} not found in environment, fetching from Google Secret Manager"
    )

    # Create the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})

    # Return the secret payload
    payload = response.payload.data.decode("UTF-8")
    return payload
