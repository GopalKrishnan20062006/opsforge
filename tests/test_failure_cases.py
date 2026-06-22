from unittest.mock import Mock, patch

from typer.testing import CliRunner

from opsforge.cli import app

runner = CliRunner()


@patch("opsforge.cli.run_preflight_checks")
def test_validate_failure(mock_checks):
    mock_checks.return_value = ["Invalid configuration"]

    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 1
    assert "Invalid configuration" in result.stdout


@patch("opsforge.cli.run_preflight_checks")
@patch("opsforge.cli.build_image")
def test_build_failure(mock_build, mock_checks):
    mock_checks.return_value = []

    mock_build.return_value = Mock(returncode=1, stderr="Docker build failed")

    result = runner.invoke(app, ["build"])

    assert result.exit_code == 1
    assert "Docker build failed" in result.stdout


@patch("opsforge.cli.load_config")
@patch("opsforge.cli.wait_for_health")
def test_health_failure(mock_health, mock_config):
    mock_health.return_value = False

    mock_config.return_value = {
        "deployment": {
            "port": 8000,
        },
        "health": {
            "endpoint": "/health",
        },
    }

    result = runner.invoke(app, ["health"])

    assert result.exit_code == 1
    assert "Service failed health check" in result.stdout
