import json
import subprocess
from datetime import datetime

from opsforge.config import load_config


def get_git_commit():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def get_git_branch():
    return subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()


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
        "artifacts": ["Dockerfile", "docker-compose.yml", "release-metadata.json"],
        "configuration": {
            "port": config["deployment"]["port"],
            "health_endpoint": config["health"]["endpoint"],
        },
        "tests": {"status": "not_implemented"},
        "lint": {"status": "not_implemented"},
    }

    return metadata


def save_metadata():

    metadata = generate_metadata()

    with open("release-metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    return metadata
