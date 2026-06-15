import time

import requests


def check_health(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return True

        return False

    except Exception:
        return False


def wait_for_health(url, retries=10, delay=3):

    for attempt in range(retries):

        if check_health(url):
            return True

        time.sleep(delay)

    return False
