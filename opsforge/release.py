import json
import subprocess
from datetime import datetime

from opsforge.config import load_config
from opsforge.quality import get_lint_summary, get_test_summary


def run_git_command(command):
    try:
        return subprocess.check_output(
            command, text=True, stderr=subprocess.DEVNULL
        ).strip()

    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        OSError,
    ):
        return None


def get_git_commit():

    commit = run_git_command(["git", "rev-parse", "HEAD"])

    return commit or "Unavailable"


def get_git_branch():

    branch = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    return branch or "Unavailable"


def get_timestamp():
    return datetime.now().isoformat()


def generate_metadata():

    config = load_config()

    metadata = {
        "service_name": config["service"]["name"],
        "service_version": config["service"]["version"],
        "docker_image": config["docker"]["image"],
        "git_commit": get_git_commit(),
        "git_branch": get_git_branch(),
        "timestamp": get_timestamp(),
        "artifacts": [
            "Dockerfile",
            "docker-compose.yml",
            "release-metadata.json",
        ],
        "configuration": {
            "port": config["deployment"]["port"],
            "health_endpoint": config["health"]["endpoint"],
        },
        "tests": get_test_summary(),
        "lint": get_lint_summary(),
    }

    return metadata


def save_metadata():

    metadata = generate_metadata()

    with open("release-metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    return metadata
