import shutil
import subprocess


def check_tool(tool_name):
    return shutil.which(tool_name) is not None


def check_docker_running():
    try:
        subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=True
        )
        return True
    except Exception:
        return False
