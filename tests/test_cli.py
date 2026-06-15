from typer.testing import CliRunner

from opsforge.cli import app

runner = CliRunner()


def test_doctor_command():

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code == 0


def test_validate_command():

    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
