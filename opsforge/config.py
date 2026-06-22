from pathlib import Path

import yaml


def load_config(path="opsforge.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


DEFAULT_CONFIG = {
    "service": {
        "name": "sample-service",
        "version": "1.0.0",
        "source_path": "sample_service",
    },
    "docker": {"image": "sample-service", "container": "sample-container"},
    "deployment": {"port": 8000},
    "health": {"endpoint": "/health"},
    "environment": {"APP_ENV": "dev"},
}


def initialize_project():

    config_file = Path("opsforge.yaml")

    if config_file.exists():
        return False

    with open(config_file, "w") as f:
        yaml.safe_dump(DEFAULT_CONFIG, f, sort_keys=False)

    Path("sample_service").mkdir(exist_ok=True)
    Path("tests").mkdir(exist_ok=True)
    Path("scripts").mkdir(exist_ok=True)

    return True
