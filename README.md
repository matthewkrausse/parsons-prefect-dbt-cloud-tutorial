# Parsons + Prefect Cloud Pipeline Template

This template provides a standardized structure for data engineers and activists to build scalable data pipelines using:

- **Parsons** for data connectors to progressive tech tools
- **Prefect** for workflow orchestration in the cloud
- **Google Cloud Platform** for infrastructure
- **dbt** for data transformation
- **Docker** for containerization
- **GitHub Actions** for CI/CD

---

```mermaid

graph TD
    A[Clone the Repository] --> B[Create Cloud Accounts]
    B --> C[Set Up Local Python Environment]
    C --> D[Authenticate with Prefect Cloud]
    D --> E[Configure GCP Authentication]
    E --> F[Set Up Required GCP Resources]
    F --> G[Configure Project Environment Variables]
    G --> H[Configure Project-Specific Settings]
    H --> I[Initial Local Test Run]
    I --> J[Set Up Prefect Cloud Infrastructure]
    J --> K[Configure CI/CD]
    K --> L[Deploy to Prefect Cloud]

    subgraph GCP Resources
        F1[Create Service Account]
        F2[Create GCS Bucket]
        F3[Enable Secret Manager]
        F4[Enable Artifact Registry]
    end
    F --> F1
    F --> F2
    F --> F3
    F --> F4

    subgraph CI/CD
        K1[Create GitHub Secrets]
        K2[Ensure Branching Strategy]
    end
    K --> K1
    K --> K2

    subgraph Project-Specific Settings
        H1[Update dbt Project Name]
        H2[Update Python Files]
        H3[Ensure Dockerfile Meets Needs]
    end
    H --> H1
    H --> H2
    H --> H3

    L --> M[Check Prefect Cloud UI for Deployed Flows]
```

## Configuration Overview

Setting up this pipeline template involves configuring credentials and settings across several services and files. This summary outlines the key areas you'll need to address, with detailed steps following in the main guide:

## IMPORTANT

Make sure to not commit any secrets, api keys, etc. to version control. the .gitignore file is set up to ignore .env files for instance. Don't hard code any sensitive keys into code.

- **Cloud Platform Accounts:** Creating accounts and enabling services/billing for Prefect Cloud and Google Cloud Platform (GCP).
- **GCP Resources:** Creating and configuring specific GCP resources like Service Accounts (with appropriate roles/permissions), Cloud Storage Buckets, Secret Manager (for storing secrets), and Artifact Registry (for Docker images).
- **Local Development Environment:** Setting up Python (`uv`, virtual environment), configuring local environment variables (like `GOOGLE_APPLICATION_CREDENTIALS`), downloading Docker Desktop, and authenticating Docker with GCP Artifact Registry (`gcloud auth configure-docker`).
- **Project `.env` File:** Populating this file with specific API keys, resource names, project IDs, and file paths required for local execution and connections (e.g., `PREFECT_API_KEY`, `PREFECT_API_URL`, `GCP_PROJECT_ID`, `GAR_LOCATION`, `GAR_REPOSITORY`, `GCS_TEMP_BUCKET`).
- **Project Code Configuration:** Updating project-specific names or settings within files like `dbt/dbt_project.yml` and potentially within Python pipeline files (`pipelines/flows/`).
- **Prefect Cloud Setup:** Logging in via the CLI and configuring Work Pools within the Prefect Cloud UI to manage execution environments.
- **GitHub Repository Settings:** Configuring GitHub Actions Secrets (e.g., `GCP_SA_KEY`, `PREFECT_API_KEY`, `GAR_LOCATION`) to allow automated CI/CD workflows to authenticate and deploy resources.

The detailed step-by-step instructions for each of these areas are provided below.

---

## Getting Fully Set Up: Step-by-Step Guide

This section outlines all the necessary steps to get your project environment, authentication, cloud resources, and CI/CD pipeline fully configured.

Follow these steps:

**1. Create a New Private Repository on GitHub:**

* Log in to your GitHub account.
* Click the `+` icon in the top-right corner and select `New repository`.
* Choose a descriptive name for your new repository (e.g., `my-dbt-prefect-project`).
* **Crucially, select `Private` visibility.** This is the most important step for keeping your version confidential.
* **Important:** **Do NOT** initialize the repository with a README, .gitignore, or license file when creating it on GitHub. You want an empty repository to push the template code into.
* Click `Create repository`.
* On the next page ("Quick setup"), copy the repository URL (either HTTPS or SSH). You will need this in Step 3. It will look something like `https://github.com/<YourUsername>/<your-repo-name>.git` or `git@github.com:<YourUsername>/<your-repo-name>.git`.

**2. Clone This Template Repository Locally:**

* Open your terminal or command prompt.
* Navigate to the directory where you want to store your project locally.
* Clone this template repository using its public URL. Replace `<your-local-directory-name>` with the name you want for your local folder (it can be the same as your GitHub repo name).
    ```bash
    git clone [https://github.com/matthewkrausse/parsons-prefect-dbt-cloud-tutorial.git](https://github.com/matthewkrausse/parsons-prefect-dbt-cloud-tutorial.git) <your-local-directory-name>
    ```
* Navigate into the newly created local directory:
    ```bash
    cd <your-local-directory-name>
    ```

**3. Connect Your Local Clone to Your New Private Repository:**

* Now, you need to tell your local Git repository to point to your new *private* repository on GitHub instead of the original public template. Replace `<your_private_repo_url>` with the URL you copied in Step 1.
    ```bash
    git remote set-url origin <your_private_repo_url>
    ```
    * *Example using HTTPS:*
        ```bash
        # git remote set-url origin [https://github.com/](https://github.com/)<YourUsername>/<your-repo-name>.git
        ```
    * *Example using SSH:*
        ```bash
        # git remote set-url origin git@github.com:<YourUsername>/<your-repo-name>.git
        ```
* **(Optional but Recommended)** Verify that the remote URL has been updated correctly:
    ```bash
    git remote -v
    ```
    *(The output should now show your private repository's URL for `origin`)*

**4. Push the Code to Your Private Repository:**

* Push the cloned code (including the template's history) from your local machine up to your new private repository on GitHub. The `-u` flag sets up tracking, making future pushes/pulls easier. (Use `main` or `master` depending on the default branch name of this template).
    ```bash
    # If the default branch is 'main'
    git push -u origin main
    ```
* You may be prompted for your GitHub username and password (or token) if using HTTPS.

**Completion:**

You're all set! Your local directory `<your-local-directory-name>` is now connected to your private GitHub repository (`<YourUsername>/<your-repo-name>`). You have an independent copy of the template code to modify and build upon privately.

**Remember:** Always handle secrets (API keys, passwords, etc.) securely using tools like GitHub Actions Secrets, environment variables, or dedicated secrets managers. **Do not commit secrets directly into your repository's files.**

**2. Create Cloud Accounts:**

- **Prefect Cloud:** Sign up for a free account at [app.prefect.cloud](https://app.prefect.cloud/).
- **Google Cloud Platform (GCP):**
  - Create a new Google Cloud Project if you don't have one already.
  - Ensure billing is enabled for the project if required by the services you intend to use (e.g., BigQuery, Cloud Storage, Secret Manager, Artifact Registry, Cloud Run).

**3. Set Up Local Python Environment:**

- Install `uv`, a fast Python package installer and resolver.
  ```bash
  pip install uv
  ```
- Create and activate a virtual environment.
  ```bash
  uv venv
  ```
  ```bash
  source .venv/bin/activate  # On macOS/Linux or .venv\Scripts\activate on Windows
  ```
- The `pyproject.toml` is where we have our project's dependencies and is where `uv` looks to know what to install
- Install project dependencies using `uv`.
  ```bash
  uv sync
  ```
- Copy the example environment file:
  ```bash
  cp .env.example .env
  ```

**4. Authenticate with Prefect Cloud:**

- Log in to your Prefect Cloud account from the command line. This will often involve opening a web browser for authentication or using an API key.

  ```bash
  prefect cloud login
  ```

- Run the healthcheck script to verify dependencies are installed correctly.
  ```bash
  python pipelines/flows/healthcheck.py
  ```

**5. Configure Google Cloud Platform (GCP) Authentication:**

- **Create a Service Account:**
  - In your GCP project, navigate to IAM & Admin > Service Accounts.
  - Create a new service account.
  - Grant the following roles (or more specific ones based on least privilege):
    - `BigQuery Data Editor` (or `BigQuery User` + `BigQuery Job User`)
    - `Storage Object Creator` (for the GCS bucket)
    - `Secret Manager Secret Accessor` (to read secrets)
    - `Artifact Registry Writer` (to push Docker images)
    - `Cloud Run Invoker` / `Cloud Run Admin` (if using Cloud Run for Prefect work pools)
    - _Add any other roles needed by your specific Parsons connectors or GCP interactions._
- **Download Service Account Key:**
  - Create a JSON key for the service account and download it securely to your local machine. **Treat this file like a password.**
- **Set Environment Variable for Local Development:**
  - Make the path to your downloaded JSON key file available via the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. How you set this depends on your OS and shell.
  - _Example (macOS/Linux, temporary for current session):_
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    ```
  - _Note:_ For production/CI/CD, you'll handle this differently (see Step 11).

**6. Set Up Required GCP Resources:**

You will need to enable these APIs. You should be prompted, if they aren't already enabled. 

- **Google Cloud Storage (GCS) Bucket:**
  - Create a GCS bucket. 'Navigation Menu' > 'Cloud Storage' > 'Buckets' > 'Create Bucket'. This is often used by BigQuery for loading data or as a temporary storage area.
  - Note the name of this bucket (e.g., `your-gcs-temp-bucket`).
- **Google Secret Manager:**
  - Enable the Secret Manager API in your GCP project. Search for 'Secret Manager' > '+ Create Secret'
  - Create secrets for sensitive information your pipelines will need (e.g., API keys for VAN, ActionNetwork, database passwords). You will reference these secret names in your code or configuration.
- **Google Artifact Registry (GAR):**
  - Enable the Artifact Registry API. '+ Create Repository' > Format: Docker > Set Region > Create
  - Create a Docker repository in GAR to store your container images. Note its location (e.g., `us-central1`) and repository name (e.g., `my-pipelines-repo`). The full path will look like: `<location>-docker.pkg.dev/<your-gcp-project-id>/<repository-name>`.

**7. Configure Project Environment Variables (`.env` file):**

- Edit the `.env` file and fill in the required values:
  - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account key file (for local runs if not set globally).
  - `GCP_PROJECT_ID`: Your Google Cloud Project ID.
  - `GCS_TEMP_BUCKET`: The name of the GCS bucket you created.
  - `GAR_LOCATION`: The location of your Artifact Registry repo (e.g., `us-central1`).
  - `GAR_REPOSITORY`: The name of your Artifact Registry repo (e.g., `my-pipelines-repo`).
  - `IMAGE_NAME`: The name of your Docker Image (e.g., `my-pipeline-image`).
  - _Add any other environment variables required by your specific pipelines or dbt connections._
  - **Important:** Ensure `.env` is listed in your `.gitignore` file to prevent accidentally committing secrets.

**8. Configure Project-Specific Settings (Code):**

- **dbt:** Optional: Rename the project in `dbt/dbt_project.yml` from the template default to your actual project name.
- **Pipelines:** Update any hardcoded GCP project IDs or resource names in the Python files within `pipelines/flows/` (though using environment variables from `.env` is preferred). Review `example_flow.py` and update lines marked with `"# CHANGE"`.
- **Docker:** Ensure your `Dockerfile` meets your project's needs.

**9. Initial Local Test Run:**

- Run the example flow locally to test connections and basic logic. This run will be tracked in the Prefect Cloud UI. If something goes wrong it's likely a issue in your `.env` file.
  ```bash
  python pipelines/flows/example_flow.py
  ```
- Check the [Prefect UI](https://app.prefect.cloud/) to see the results of your local flow run.

**10. Set Up Prefect Cloud Infrastructure (Work Pools):**

- Create work pools in Prefect Cloud to manage the infrastructure where your flows will run when deployed. This template assumes serverless execution (like Google Cloud Run).
- [Follow the steps here to create two work pools, e.g., "prod-cloud-work-pool" and "dev-cloud-work-pool"](https://docs.prefect.io/v3/deploy/infrastructure-examples/serverless). Adjust names as needed, but ensure they match deployment configurations. These work pools will likely point to the Docker image you'll build and push (either locally or via CI/CD).

**11. Configure CI/CD (GitHub Actions Secrets):**

- **GitHub Secrets:** In your GitHub repository, go to `Settings > Secrets and variables > Actions`. Create the following **Repository Secrets**:
  - `GOOGLE_APPLICATION_CREDENTIALS`: The _entire content_ of your downloaded GCP service account JSON key file. (Used to push to Google Artifact Registry or interact with GCP)
  - `GCP_PROJECT_ID`: Your Google Cloud Project ID.
  - `GCS_TEMP_BUCKET`: The name of the GCS bucket you created.
  - `GAR_LOCATION`: The location of your Artifact Registry repo (e.g., `us-central1`).
  - `GAR_REPOSITORY`: The name of your Artifact Registry repo (e.g., `my-pipelines-repo`).
  - `IMAGE_NAME`: The name of your Docker Image (e.g., `my-pipeline-image`).
  - `PREFECT_API_KEY`: [Your Prefect Cloud API key.](https://app.prefect.cloud/my/api-keys)
  - `PREFECT_API_URL`: Your Prefect Cloud workspace API URL. (run `prefect config view` in the terminal to get your URL)
- **Branching Strategy:** The CI/CD is often configured to trigger on specific branches (e.g., `dev`, `main`). Ensure your branching strategy aligns with the triggers in `.github/workflows/*.yaml`. The example suggests creating a `dev` branch and opening a Pull Request.

**12. Deploy to Prefect Cloud via CI/CD:**

- Commit your changes (ensure `.env` is gitignored!) and any code modifications.

You can manually trigger these Workflows in Actions. When you want to change the code, create a branch and follow the below steps.
- Create a branch (e.g., `dev` if that's what your workflow triggers on).
  ```bash
  git checkout -b dev
  git add .
  git commit -m "Initial setup and configuration"
  git push origin dev
  ```
- Open a Pull Request on GitHub from your `dev` branch to your main branch (or as configured in `deploy_flow.yaml`).
- The GitHub Actions workflow (`deploy_flow.yaml`) should automatically trigger. It will typically:
  - Authenticate Docker with Google Artifact Registry.
  - Build a Docker image containing your flow code and dependencies using the `Dockerfile`.
  - Push the Docker image to your specified Google Artifact Registry repository.
  - Run the `pipelines/flows/deploy_flows.py` script, which registers your flows with Prefect Cloud and associates them with the appropriate work pool and image.
- Once the action completes successfully, go to the Prefect Cloud UI. You should see your deployed flows under "Deployments". You can now trigger runs directly from the UI, which will execute using the pushed Docker image on the infrastructure defined by your work pool (e.g., Google Cloud Run). If running locally, you must build and push the Docker Image yourself.

- You can also go to your logs in Google Cloud to check that it ran in the cloud!

You have now completed the full setup process!

---

## Building and Pushing the Docker Image Locally (Optional)

While the CI/CD pipeline (`deploy_flow.yaml`) handles building and pushing the Docker image automatically, you might want to do this manually for testing the container environment or for deployments outside the standard CI/CD process.

Our Dockerfile is a bit complex but its effecient and helps reduce build time.

**Prerequisites:**

- Docker Desktop or Docker Engine installed and running on your local machine.
- Google Cloud CLI (`gcloud`) installed.
- You have completed the GCP setup steps above, including creating a Service Account, enabling Artifact Registry, and creating a repository.

**Steps:**

1.  **Authenticate Docker with Google Artifact Registry (GAR):**
    Configure Docker to use your Google Cloud credentials for authentication with Artifact Registry. Replace `<location>` with your GAR repository's location (e.g., `us-central1`).

    ```bash
    gcloud auth configure-docker <location>-docker.pkg.dev
    ```

    _Note: You might need to log in to gcloud first (`gcloud auth login`) or ensure your environment is using the correct service account (`gcloud auth activate-service-account --key-file=/path/to/your/keyfile.json`)._

2.  **Define Image Name and Tag:**
    Choose a name and tag for your image. It's best practice to include the full GAR path. Replace placeholders accordingly.

    ```bash
    # Ensure these match your .env file or actual values
    export GCP_PROJECT_ID="<your-gcp-project-id>"
    export GAR_LOCATION="<your-gar-location>" # e.g., us-central1
    export GAR_REPOSITORY="<your-gar-repository-name>" # e.g., my-pipelines-repo
    export IMAGE_NAME="<your-image-name>" # e.g., parsons-prefect-pipeline
    export IMAGE_TAG="<your-tag>" # e.g., latest, v1.0, git sha

    export FULL_IMAGE_NAME="${GAR_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${GAR_REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"
    echo "Building image: ${FULL_IMAGE_NAME}"
    ```

3.  **Build the Docker Image:**

    First, Docker Desktop needs to be installed and running.

    Run the build command from the root directory of your project (where the `Dockerfile` is located).

    ```bash
    docker build -t "${FULL_IMAGE_NAME}" .
    ```

    _Note: If your Dockerfile needs access to secrets or arguments at build time (less common for Prefect flows, more common for application builds), you might need to use `--build-arg`. For runtime secrets, rely on environment variables or Prefect Blocks/GCP Secret Manager._

4.  **Push the Docker Image to GAR:**
    Once the build is successful, push the image to your Artifact Registry repository.
    ```bash
    docker push "${FULL_IMAGE_NAME}"
    ```

Now the image is available in your Google Artifact Registry repository. You could potentially update a Prefect Deployment manually in the UI to use this specific image tag, or use this image for local testing with Docker.

---

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

## Using dbt (optional)

I added a dbt folder in here for transformations.
You can configure it to create a model of the dataset we just created in BQ.
But you never have to use it.

```bash
cd dbt
dbt deps         # Install package dependencies
dbt run          # Run all models
dbt test         # Run all tests
```

