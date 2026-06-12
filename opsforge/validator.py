from pathlib import Path
from opsforge.config import load_config


def validate_files():
    errors = []

    required_files = [
        "opsforge.yaml",
        "Dockerfile",
        "docker-compose.yml"
    ]

    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Missing file: {file}")

    return errors


def validate_config():
    errors = []

    try:
        config = load_config()
    except Exception as e:
        return [f"Invalid YAML: {e}"]

    required_fields = [
        ("service", "name"),
        ("service", "version"),
        ("service", "source_path"),
        ("docker", "image"),
        ("docker", "container"),
        ("deployment", "port"),
        ("health", "endpoint"),
    ]

    for section, key in required_fields:
        if section not in config:
            errors.append(f"Missing section: {section}")
            continue

        if key not in config[section]:
            errors.append(f"Missing field: {section}.{key}")

    return errors


def validate_port(port):
    errors = []

    if not (1 <= port <= 65535):
        errors.append("Port must be between 1 and 65535")
        return errors

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind(("localhost", port))
    except OSError:
        errors.append(f"Port {port} already in use")

    sock.close()

    return errors
