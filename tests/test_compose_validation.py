from unittest.mock import patch

from opsforge.validator import validate_compose_matches


@patch("opsforge.validator.load_compose")
def test_compose_matches(mock_load_compose):
    mock_load_compose.return_value = {
        "services": {
            "sample-service": {
                "image": "sample-service",
                "ports": ["8000:8000"],
            }
        }
    }

    config = {
        "docker": {
            "image": "sample-service",
        },
        "deployment": {
            "port": 8000,
        },
    }

    assert validate_compose_matches(config) == []


@patch("opsforge.validator.load_compose")
def test_compose_port_mismatch(mock_load_compose):
    mock_load_compose.return_value = {
        "services": {
            "sample-service": {
                "image": "sample-service",
                "ports": ["9000:8000"],
            }
        }
    }

    config = {
        "docker": {
            "image": "sample-service",
        },
        "deployment": {
            "port": 8000,
        },
    }

    errors = validate_compose_matches(config)

    assert any("Port mismatch" in error for error in errors)


@patch("opsforge.validator.load_compose")
def test_compose_image_mismatch(mock_load_compose):
    mock_load_compose.return_value = {
        "services": {
            "sample-service": {
                "image": "wrong-image",
                "ports": ["8000:8000"],
            }
        }
    }

    config = {
        "docker": {
            "image": "sample-service",
        },
        "deployment": {
            "port": 8000,
        },
    }

    errors = validate_compose_matches(config)

    assert any("Docker image mismatch" in error for error in errors)


@patch("opsforge.validator.load_compose")
def test_missing_compose_file(mock_load_compose):
    mock_load_compose.return_value = None

    config = {
        "docker": {
            "image": "sample-service",
        },
        "deployment": {
            "port": 8000,
        },
    }

    errors = validate_compose_matches(config)

    assert "docker-compose.yml not found." in errors
