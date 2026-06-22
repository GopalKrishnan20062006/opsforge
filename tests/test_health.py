from unittest.mock import Mock, patch

import requests

from opsforge.health import check_health, wait_for_health


@patch("opsforge.health.requests.get")
def test_check_health_success(mock_get):
    response = Mock()
    response.status_code = 200
    mock_get.return_value = response

    result = check_health("http://localhost:8000/health")

    assert result["healthy"] is True
    assert result["status_code"] == 200
    assert result["error"] is None


@patch("opsforge.health.requests.get")
def test_check_health_failure(mock_get):
    response = Mock()
    response.status_code = 500
    mock_get.return_value = response

    result = check_health("http://localhost:8000/health")

    assert result["healthy"] is False
    assert result["status_code"] == 500


@patch("opsforge.health.requests.get")
def test_check_health_timeout(mock_get):
    mock_get.side_effect = requests.Timeout

    result = check_health("http://localhost:8000/health")

    assert result["healthy"] is False
    assert result["error"] == "Health check timed out"


@patch("opsforge.health.requests.get")
def test_check_health_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("Connection refused")

    result = check_health("http://localhost:8000/health")

    assert result["healthy"] is False
    assert result["status_code"] is None


@patch("opsforge.health.check_health")
def test_wait_for_health_success(mock_check):
    mock_check.return_value = {"healthy": True}

    assert wait_for_health("http://localhost", retries=3, delay=0)


@patch("opsforge.health.check_health")
def test_wait_for_health_failure(mock_check):
    mock_check.return_value = {"healthy": False}

    assert not wait_for_health("http://localhost", retries=3, delay=0)
