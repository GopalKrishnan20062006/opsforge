from unittest.mock import Mock, patch

from typer.testing import CliRunner

from opsforge.cli import app

runner = CliRunner()


@patch("opsforge.cli.run_preflight_checks")
@patch("opsforge.cli.build_image")
@patch("opsforge.cli.deploy_service")
@patch("opsforge.cli.check_health")
@patch("opsforge.cli.load_config")
@patch("opsforge.cli.destroy_service")
def test_complete_lifecycle(
    mock_destroy,
    mock_load_config,
    mock_health,
    mock_deploy,
    mock_build,
    mock_checks,
):
    mock_checks.return_value = []

    mock_build.return_value = Mock(returncode=0)

    mock_deploy.return_value = Mock(returncode=0)

    mock_health.return_value = {
        "healthy": True,
        "status_code": 200,
        "error": None,
    }

    mock_load_config.return_value = {
        "deployment": {
            "port": 8000,
        },
        "health": {
            "endpoint": "/health",
        },
        "docker": {
            "container": "sample-container",
        },
    }

    mock_destroy.return_value = Mock(returncode=0)

    assert runner.invoke(app, ["validate"]).exit_code == 0
    assert runner.invoke(app, ["build"]).exit_code == 0
    assert runner.invoke(app, ["deploy"]).exit_code == 0
    assert runner.invoke(app, ["destroy"]).exit_code == 0
