from unittest.mock import Mock, patch

from typer.testing import CliRunner

from opsforge.cli import app

runner = CliRunner()


@patch("opsforge.cli.check_tool")
@patch("opsforge.cli.check_docker_running")
def test_doctor_command(mock_running, mock_tool):
    mock_tool.return_value = True
    mock_running.return_value = True

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code == 0
    assert "Python" in result.stdout
    assert "Docker daemon running" in result.stdout


@patch("opsforge.cli.run_preflight_checks")
def test_validate_command(mock_checks):
    mock_checks.return_value = []

    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
    assert "Validation successful" in result.stdout


@patch("opsforge.cli.run_preflight_checks")
@patch("opsforge.cli.build_image")
def test_build_command(mock_build, mock_checks):
    mock_checks.return_value = []

    mock_build.return_value = Mock(returncode=0, stdout="Build successful")

    result = runner.invoke(app, ["build"])

    assert result.exit_code == 0
    assert "Docker image built successfully" in result.stdout


@patch("opsforge.cli.get_status")
def test_status_command(mock_status):
    mock_status.return_value = Mock(returncode=0, stdout="Container is running")

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Container is running" in result.stdout


@patch("opsforge.cli.get_logs")
def test_logs_command(mock_logs):
    mock_logs.return_value = Mock(returncode=0, stdout="Application started")

    result = runner.invoke(app, ["logs"])

    assert result.exit_code == 0
    assert "Application started" in result.stdout
