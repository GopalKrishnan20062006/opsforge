from opsforge.release import generate_metadata


def mock_release_dependencies(mocker):
    mocker.patch(
        "opsforge.release.load_config",
        return_value={
            "service": {
                "name": "sample-service",
                "version": "1.0.0",
            },
            "docker": {
                "image": "sample-service",
            },
            "deployment": {
                "port": 8000,
            },
            "health": {
                "endpoint": "/health",
            },
        },
    )

    mocker.patch("opsforge.release.get_git_commit", return_value="abc123")
    mocker.patch("opsforge.release.get_git_branch", return_value="main")
    mocker.patch("opsforge.release.get_timestamp", return_value="2025-01-01T00:00:00")
    mocker.patch("opsforge.release.get_test_summary", return_value={"status": "passed"})
    mocker.patch("opsforge.release.get_lint_summary", return_value={"status": "passed"})


def test_release_contains_required_fields(mocker):
    mock_release_dependencies(mocker)

    metadata = generate_metadata()

    required_fields = [
        "service_name",
        "service_version",
        "docker_image",
        "git_commit",
        "git_branch",
        "timestamp",
        "artifacts",
        "configuration",
        "tests",
        "lint",
    ]

    for field in required_fields:
        assert field in metadata


def test_git_metadata(mocker):
    mock_release_dependencies(mocker)

    metadata = generate_metadata()

    assert metadata["git_commit"] == "abc123"
    assert metadata["git_branch"] == "main"


def test_service_metadata(mocker):
    mock_release_dependencies(mocker)

    metadata = generate_metadata()

    assert metadata["service_name"] == "sample-service"
    assert metadata["service_version"] == "1.0.0"
    assert metadata["docker_image"] == "sample-service"


def test_configuration_metadata(mocker):
    mock_release_dependencies(mocker)

    metadata = generate_metadata()

    assert metadata["configuration"]["port"] == 8000
    assert metadata["configuration"]["health_endpoint"] == "/health"


def test_artifacts_metadata(mocker):
    mock_release_dependencies(mocker)

    metadata = generate_metadata()

    assert "Dockerfile" in metadata["artifacts"]
    assert "docker-compose.yml" in metadata["artifacts"]
