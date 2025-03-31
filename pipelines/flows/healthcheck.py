import platform
import prefect
from prefect import task, flow
import sys


@task(log_prints=True)
def log_platform_info(env=None):
    print("Environment = %s", env)
    print("Host's network name = %s", platform.node())
    print("Python version = %s", platform.python_version())
    print("Platform information (instance type) = %s ", platform.platform())
    print("OS/Arch = %s/%s", sys.platform, platform.machine())
    print("Prefect Version = %s 🚀", prefect.__version__)


@flow
def healthcheck(env=None):
    """
    Healthcheck flow to log platform information and environment details.
    """
    log_platform_info(env=env)


if __name__ == "__main__":
    healthcheck()
