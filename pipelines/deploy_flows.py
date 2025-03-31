"""
Script to deploy Parsons + Prefect flows to a work pool.
"""
from flows.example_flow import example_pipeline
# Import additional flows here

from prefect.docker import DockerImage
import os
import dotenv

from pipelines.utilities import determine_git_environment

dotenv.load_dotenv()

# Determine environment (prod or dev)
environment = os.environ.get("ENVIRONMENT")
if environment:
    print(f"Using environment from ENVIRONMENT variable: {environment}")
else:
    # Fall back to git-based detection if environment variable is not set
    environment = determine_git_environment()
    print(f"Determined environment from git: {environment}")

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

branch_name = os.environ.get("BRANCH_NAME", "local")
is_prod = environment == "prod"

print(
    f"Deploying with environment: {environment}, is_prod: {is_prod}, branch: {branch_name}"
)

# Set up environment-specific configurations
image_name = f"parsons-prefect-{environment}"  # Updated image name to reflect purpose
image_tag = os.environ.get("TAG", "latest")
full_image_name = (
    f"us-central1-docker.pkg.dev/{PROJECT_ID}/prefect-images/{image_name}:{image_tag}" # Change to your image registry/project_id etc.
)

# Configure work pool based on environment
work_pool_name = "prod-cloud-run-pool" if is_prod else "dev-cloud-run-pool"

# Define a list of flows to deploy
flows_to_deploy = [
    {
        "flow": example_pipeline,
        "name": "Parsons Data Pipeline Example",
        "schedule": "0 0 * * *",  # Daily at midnight
    },
    # Add additional flows to deploy here
    # Example:
    # {
    #     "flow": voter_sync_pipeline,
    #     "name": "VAN Voter Sync Pipeline",
    #     "schedule": "0 12 * * *",  # Daily at noon
    # },
]

if __name__ == "__main__":
    for flow_config in flows_to_deploy:
        flow = flow_config["flow"]
        base_deployment_name = flow_config["name"]
        # Configure the schedule for the flow
        schedule = flow_config["schedule"] if is_prod else None

        # Create deployment name with environment prefix
        deployment_name = base_deployment_name
        if not is_prod:
            deployment_name = f"DEV-{deployment_name}"

        # Environment-specific parameters
        flow_parameters = {"env": environment}

        print(f"Deploying {deployment_name} with parameters: {flow_parameters}")

        flow.deploy(
            name=deployment_name,
            work_pool_name=work_pool_name,
            image=DockerImage(
                name=full_image_name,
                platform="linux/amd64",
            ),
            build=False,
            push=False,
            cron=schedule,
            parameters={"env": environment},
            tags=[environment, branch_name],
        )
