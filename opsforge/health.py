import time

import requests


def check_health(url):
    try:
        response = requests.get(url, timeout=2)

        return {
            "healthy": response.status_code == 200,
            "status_code": response.status_code,
            "error": None,
        }

    except requests.Timeout:
        return {
            "healthy": False,
            "status_code": None,
            "error": "Health check timed out",
        }

    except requests.RequestException as e:
        return {
            "healthy": False,
            "status_code": None,
            "error": str(e),
        }


def wait_for_health(url, retries=10, delay=3):

    for _ in range(retries):

        result = check_health(url)

        if result["healthy"]:
            return True

        time.sleep(delay)

    return False
