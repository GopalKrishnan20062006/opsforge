from opsforge.release import generate_metadata


def test_release_contains_required_fields():

    metadata = generate_metadata()

    required_fields = [
        "service_name",
        "service_version",
        "docker_image",
        "git_commit",
        "git_branch",
        "timestamp",
    ]

    for field in required_fields:
        assert field in metadata


def test_git_metadata(mocker):

    mocker.patch("opsforge.release.get_git_commit", return_value="abc123")

    mocker.patch("opsforge.release.get_git_branch", return_value="main")

    metadata = generate_metadata()

    assert metadata["git_commit"] == "abc123"
    assert metadata["git_branch"] == "main"
