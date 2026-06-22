import shutil
import subprocess

from opsforge.validator import validate_config, validate_files


def run_preflight_checks():
    errors = []

    errors.extend(validate_files())
    errors.extend(validate_config())

    return errors


def check_tool(tool_name):
    return shutil.which(tool_name) is not None


def check_docker_running():
    try:
        subprocess.run(["docker", "info"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def check_docker():
    if not check_tool("docker"):
        return "Docker is not installed."

    if not check_docker_running():
        return "Docker daemon is not running."

    return None
