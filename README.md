# Parsons + Prefect Cloud Pipeline Template

This template provides a standardized structure for data engineers and activists to build scalable data pipelines using:

- **Parsons** for data connectors to progressive tech tools
- **Prefect** for workflow orchestration in the cloud
- **Google Cloud Platform** for infrastructure
- **dbt** for data transformation
- **Docker** for containerization
- **GitHub Actions** for CI/CD

## What is Parsons?

[Parsons](https://github.com/move-coop/parsons) is an open-source Python package that provides connectors to dozens of data sources and tools used in the progressive data ecosystem, including:

- **VAN/EveryAction**
- **ActionNetwork**
- **ActBlue**
- **Redshift/Postgres/MySQL** databases
- **Google Sheets and BigQuery**
- **And many more!**

## Project Structure

```
project/
├── dbt/                        # Data modeling with dbt
│   ├── models/                 # SQL transformation models
│   └── dbt_project.yml         # dbt project configuration
├── pipelines/                  # Prefect data pipelines
│   ├── flows/                  # Workflow definitions
│   └── deploy_flows.py         # Flow deployment script
├── tests/                      # Unit and integration tests
├── .github/workflows/          # CI/CD pipeline configurations
├── Dockerfile                  # Container configuration
├── pyproject.toml              # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

## Getting Started

1. Clone this template

2. Update project-specific configurations:

   - Rename project in `dbt_project.yml`
   - Update GCP project info in pipeline files
   - Customize models and pipelines as needed

3. Set up Python environment:

   ```bash
   # Install uv
   pip install uv

   # Create virtual environment
   uv venv

   # Activate the environment
   source .venv/bin/activate  # On macOS/Linux
   # or .venv\Scripts\activate on Windows

   # Install dependencies
   uv sync
   ```

4. Copy `.env.example` to `.env` and fill in your environment variables

5. Configure GCP authentication:

   - Create service account with appropriate permissions
   - Download JSON key file
   - Set path in GOOGLE_APPLICATION_CREDENTIALS environment variable
   - Create and add a gcs_temp_bucket for BigQuery Copying, add as env var or hard code

6. Set Prefect Creds in .env or use the CLI to login

   - `prefect cloud login`
   - Login in using the web browser or api key

7. Review example_flow.py and update any lines that have a comment "CHANGE"

8. Run example_flow.py

   - `python pipelines/flows/example_flow.py`

9. This just ran locally but everything is tracked using the [Prefect UI](https://app.prefect.cloud/).
   Let's go take a look.

10. Let's run it in the Cloud

11. Create Prefect Work Pools

-

## Using dbt

```bash
cd dbt
dbt deps         # Install package dependencies
dbt run          # Run all models
dbt test         # Run all tests
```

## Using Prefect

```bash
# Run a flow locally
python pipelines/flows/example_flow.py

# Deploy flows
python pipelines/deploy_flows.py
```

## Deploying with CI/CD

The template includes GitHub Actions workflows:

- `deploy_flow.yaml`: Build/deploy Prefect flows
- `dbt_run.yml`: Build/test dbt models on PRs
- `dbt_hourly.yml`: Scheduled dbt runs

Required GitHub Secrets:

- GCP_PROJECT_ID
- GCP_SA_KEY
- PREFECT_API_KEY
- PREFECT_API_URL
- GOOGLE_CREDENTIALS_DOCKER

## Customization Guide

1. **Project Configuration**

   - Update project name in `dbt_project.yml`
   - Set your GCP project ID in pipeline files
   - Configure database/data warehouse connections

2. **Data Sources**

   - Define your sources in `dbt/models/sources.yml`
   - Create appropriate staging models

3. **Pipelines**

   - Customize flow files in `pipelines/flows/`
   - Update deployment configuration as needed

4. **CI/CD**

   - Adjust GitHub Actions workflows based on your needs
   - Configure proper triggers and schedules

5. **Testing**
   - Add unit and integration tests in the `tests/` directory
   - Use pytest or other testing frameworks
   - Ensure coverage for critical components

## Best Practices

- Name models and pipelines consistently
- Document data lineage and transformations
- Follow a clear pattern for directory structure
- Use environment variables for sensitive information
- Test your models to ensure data quality
