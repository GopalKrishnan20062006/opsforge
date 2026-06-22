from unittest.mock import patch

from opsforge.doctor import (
    check_docker,
    check_docker_running,
    check_tool,
)


@patch("opsforge.doctor.shutil.which")
def test_check_tool_found(mock_which):
    mock_which.return_value = "/usr/bin/docker"

    assert check_tool("docker") is True


@patch("opsforge.doctor.shutil.which")
def test_check_tool_not_found(mock_which):
    mock_which.return_value = None

    assert check_tool("docker") is False


@patch("opsforge.doctor.subprocess.run")
def test_check_docker_running(mock_run):
    mock_run.return_value = None

    assert check_docker_running() is True


@patch("opsforge.doctor.subprocess.run")
def test_check_docker_not_running(mock_run):
    mock_run.side_effect = Exception()

    assert check_docker_running() is False


@patch("opsforge.doctor.check_tool")
@patch("opsforge.doctor.check_docker_running")
def test_check_docker_success(mock_running, mock_tool):
    mock_tool.return_value = True
    mock_running.return_value = True

    assert check_docker() is None


@patch("opsforge.doctor.check_tool")
def test_check_docker_not_installed(mock_tool):
    mock_tool.return_value = False

    assert check_docker() == "Docker is not installed."


@patch("opsforge.doctor.check_tool")
@patch("opsforge.doctor.check_docker_running")
def test_check_docker_daemon_not_running(mock_running, mock_tool):
    mock_tool.return_value = True
    mock_running.return_value = False

    assert check_docker() == "Docker daemon is not running."
