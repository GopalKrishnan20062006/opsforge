from opsforge.docker_ops import build_image, deploy_service


def test_build_failure(mocker):

    mock_result = mocker.Mock()

    mock_result.returncode = 1
    mock_result.stderr = "Build failed"

    mocker.patch("subprocess.run", return_value=mock_result)

    result = build_image()

    assert result.returncode == 1


def test_deploy_failure(mocker):

    mock_result = mocker.Mock()

    mock_result.returncode = 1
    mock_result.stderr = "Deploy failed"

    mocker.patch("subprocess.run", return_value=mock_result)

    result = deploy_service()

    assert result.returncode == 1
