from pathlib import Path

import yaml

from opsforge.config import load_config


def validate_files():
    errors = []

    required_files = ["opsforge.yaml", "Dockerfile", "docker-compose.yml"]

    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Missing file: {file}")

    return errors


def validate_types(config):
    errors = []

    service = config.get("service", {})
    docker = config.get("docker", {})
    deployment = config.get("deployment", {})
    health = config.get("health", {})
    environment = config.get("environment", {})

    if not isinstance(service.get("name"), str):
        errors.append("service.name must be a string.")

    if not isinstance(service.get("version"), str):
        errors.append("service.version must be a string.")

    if not isinstance(service.get("source_path"), str):
        errors.append("service.source_path must be a string.")

    if not isinstance(docker.get("image"), str):
        errors.append("docker.image must be a string.")

    if not isinstance(docker.get("container"), str):
        errors.append("docker.container must be a string.")

    if not isinstance(deployment.get("port"), int):
        errors.append("deployment.port must be an integer.")

    if not isinstance(health.get("endpoint"), str):
        errors.append("health.endpoint must be a string.")

    if not isinstance(environment, dict):
        errors.append("environment must be a dictionary.")

    return errors


def validate_required_fields(config):
    errors = []

    required_fields = [
        ("service", "name"),
        ("service", "version"),
        ("service", "source_path"),
        ("docker", "image"),
        ("docker", "container"),
        ("deployment", "port"),
        ("health", "endpoint"),
        ("environment", None),
    ]

    for section, field in required_fields:

        if section not in config:
            errors.append(f"Missing section: {section}")
            continue

        if field is not None and field not in config[section]:
            errors.append(f"Missing field: {section}.{field}")

    return errors


def validate_source_path(config):
    errors = []

    source_path = config["service"]["source_path"]

    path = Path(source_path)

    if not path.exists():
        errors.append(f"Source path does not exist: {source_path}")

    elif not path.is_dir():
        errors.append(f"Source path is not a directory: {source_path}")

    return errors


def validate_config():
    config = load_config()

    errors = []

    errors.extend(validate_required_fields(config))

    errors.extend(validate_types(config))

    errors.extend(validate_port(config))

    errors.extend(validate_source_path(config))

    errors.extend(validate_health_endpoint(config))

    errors.extend(validate_environment(config))

    errors.extend(validate_docker_config(config))
    errors.extend(validate_compose_matches(config))

    return errors


def validate_port(config):
    errors = []

    port = config["deployment"]["port"]

    if not isinstance(port, int):
        return errors

    if port < 1 or port > 65535:
        errors.append("Port must be between 1 and 65535.")

    return errors


def validate_health_endpoint(config):
    errors = []

    endpoint = config["health"]["endpoint"]

    if not endpoint.startswith("/"):
        errors.append("health.endpoint must start with '/'.")

    return errors


def validate_docker_config(config):
    errors = []

    docker = config["docker"]

    image = docker["image"]
    container = docker["container"]

    if not image.strip():
        errors.append("Docker image name cannot be empty.")

    if not container.strip():
        errors.append("Container name cannot be empty.")

    return errors


def validate_environment(config):
    errors = []

    environment = config["environment"]

    if not isinstance(environment, dict):
        errors.append("environment must be a dictionary.")
        return errors

    for key, value in environment.items():

        if not isinstance(key, str):
            errors.append("Environment variable names must be strings.")

        if not isinstance(value, str):
            errors.append(f"Environment variable '{key}' must have a string value.")

    return errors


def load_compose():
    compose_file = Path("docker-compose.yml")

    if not compose_file.exists():
        return None

    with open(compose_file) as f:
        return yaml.safe_load(f)


def validate_compose_matches(config):
    errors = []

    compose = load_compose()

    if compose is None:
        errors.append("docker-compose.yml not found.")
        return errors

    try:
        service = next(iter(compose["services"].values()))

        compose_ports = service.get("ports", [])

        if not compose_ports:
            errors.append("No port mapping found.")
        else:
            port_mapping = compose_ports[0]
            host_port = int(port_mapping.split(":")[0])

            expected_port = config["deployment"]["port"]

            if host_port != expected_port:
                errors.append(
                    f"Port mismatch "
                    f"(opsforge.yml={expected_port}, "
                    f"docker-compose.yml={host_port})"
                )

        compose_image = service.get("image")
        expected_image = config["docker"]["image"]

        if compose_image != expected_image:
            errors.append(
                f"Docker image mismatch "
                f"(opsforge.yml='{expected_image}', "
                f"docker-compose.yml='{compose_image}')"
            )

    except (KeyError, IndexError, ValueError, StopIteration):
        errors.append(
            "docker-compose.yml is missing required service "
            "or has an invalid configuration."
        )

    return errors
