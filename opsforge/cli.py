import subprocess

import typer

from opsforge.config import load_config
from opsforge.docker_ops import (
    build_image,
    deploy_service,
    destroy_service,
    get_logs,
    get_status,
)
from opsforge.doctor import check_docker_running, check_tool
from opsforge.health import wait_for_health
from opsforge.release import save_metadata
from opsforge.validator import validate_config, validate_files, validate_port

app = typer.Typer()


@app.command()
def doctor():
    tools = [
        ("python3", "Python"),
        ("git", "Git"),
        ("docker", "Docker"),
        ("make", "Make"),
    ]

    for cmd, name in tools:
        if check_tool(cmd):
            print(f"✓ {name}")
        else:
            print(f"✗ {name}")

    if check_docker_running():
        print("✓ Docker daemon running")
    else:
        print("✗ Docker daemon not running")


@app.command()
def hello():
    print("Hello")


@app.command()
def validate():
    errors = []

    errors.extend(validate_files())
    errors.extend(validate_config())

    try:
        config = load_config()
        port = config["deployment"]["port"]
        errors.extend(validate_port(port))
    except Exception:
        pass

    if errors:
        print("\nValidation Failed:\n")

        for error in errors:
            print(f"✗ {error}")

        raise typer.Exit(code=1)

    print("✓ Validation successful")


@app.command()
def build():

    errors = []

    errors.extend(validate_files())
    errors.extend(validate_config())

    if errors:
        print("Validation failed")

        for error in errors:
            print(f"✗ {error}")

        raise typer.Exit(code=1)

    result = build_image()

    if result.returncode == 0:
        print("✓ Docker image built successfully")
    else:
        print("✗ Build failed")
        print(result.stderr)

        raise typer.Exit(code=1)


@app.command()
def deploy():
    result = deploy_service()

    if result.returncode == 0:
        print("✓ Service deployed")
    else:
        print("✗ Deployment failed")
        print(result.stderr)

        raise typer.Exit(code=1)


@app.command()
def health():

    config = load_config()

    port = config["deployment"]["port"]

    endpoint = config["health"]["endpoint"]

    url = f"http://localhost:{port}{endpoint}"

    if wait_for_health(url):
        print("✓ Service is healthy")
    else:
        print("✗ Service failed health check")

        raise typer.Exit(code=1)


@app.command()
def status():

    result = get_status()

    if result.returncode != 0:
        print("Failed to get status")
        raise typer.Exit(code=1)

    print(result.stdout)


@app.command()
def logs():

    result = get_logs()

    if result.returncode != 0:
        print("Failed to fetch logs")
        raise typer.Exit(code=1)

    print(result.stdout)


@app.command()
def destroy():

    result = destroy_service()

    if result.returncode == 0:
        print("✓ Deployment removed")
    else:
        print("✗ Destroy failed")
        print(result.stderr)

        raise typer.Exit(code=1)


@app.command()
def release():

    metadata = save_metadata()

    print("✓ Release metadata generated")

    print(f"Version: {metadata['service_version']}")


@app.command()
def test():

    result = subprocess.run(["pytest"], text=True)

    raise typer.Exit(code=result.returncode)


if __name__ == "__main__":
    app()
