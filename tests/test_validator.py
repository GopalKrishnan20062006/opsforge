from opsforge.validator import validate_port


def test_valid_port():
    errors = validate_port(8000)

    assert errors == []


def test_invalid_port_too_high():
    errors = validate_port(70000)

    assert len(errors) > 0


def test_invalid_port_negative():
    errors = validate_port(-1)

    assert len(errors) > 0
