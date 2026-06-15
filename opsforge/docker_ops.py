import subprocess


def build_image():
    result = subprocess.run(
        ["docker", "compose", "build"], capture_output=True, text=True
    )
    return result


def deploy_service():
    return subprocess.run(
        ["docker", "compose", "up", "-d"], capture_output=True, text=True
    )


def get_status():
    return subprocess.run(["docker", "ps"], capture_output=True, text=True)


def get_logs():
    return subprocess.run(["docker", "compose", "logs"], capture_output=True, text=True)


def destroy_service():
    return subprocess.run(["docker", "compose", "down"], capture_output=True, text=True)
