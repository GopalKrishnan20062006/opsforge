import subprocess


def build_image():
    result = subprocess.run(["docker", "compose", "build"], text=True)
    return result


def deploy_service():
    return subprocess.run(
        ["docker", "compose", "up", "-d"], capture_output=True, text=True
    )


def get_status():
    return subprocess.run(
        ["docker", "compose", "ps"],
        capture_output=True,
        text=True,
    )


def get_logs():
    return subprocess.run(
        ["docker", "compose", "logs"],
        capture_output=True,
        text=True,
    )


def get_container_status(container_name):

    result = subprocess.run(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"name={container_name}",
            "--format",
            "{{.Status}}",
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip() or "Container not found"


def get_recent_logs(container_name, lines=20):

    result = subprocess.run(
        ["docker", "logs", "--tail", str(lines), container_name],
        capture_output=True,
        text=True,
    )

    return result.stdout or result.stderr


def destroy_service():
    return subprocess.run(["docker", "compose", "down"], capture_output=True, text=True)
