import requests

from opsforge.health import check_health


def test_health_success(mocker):

    mock_response = mocker.Mock()
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    assert check_health("http://localhost:8000/health") is True


def test_health_failure_status(mocker):

    mock_response = mocker.Mock()
    mock_response.status_code = 500

    mocker.patch("requests.get", return_value=mock_response)

    assert check_health("http://localhost:8000/health") is False


def test_health_exception(mocker):

    mocker.patch("requests.get", side_effect=requests.exceptions.ConnectionError)

    assert check_health("http://localhost:8000/health") is False
