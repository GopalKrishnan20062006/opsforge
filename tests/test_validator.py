from opsforge.validator import validate_port


def test_valid_port():
    config = {"deployment": {"port": 8000}}

    errors = validate_port(config)

    assert errors == []


def test_invalid_port_too_high():
    config = {"deployment": {"port": 70000}}

    errors = validate_port(config)

    assert errors == ["Port must be between 1 and 65535."]


def test_invalid_port_negative():
    config = {"deployment": {"port": -1}}

    errors = validate_port(config)

    assert errors == ["Port must be between 1 and 65535."]


def test_valid_port_lower_boundary():
    config = {"deployment": {"port": 1}}

    assert validate_port(config) == []


def test_valid_port_upper_boundary():
    config = {"deployment": {"port": 65535}}

    assert validate_port(config) == []


def test_non_integer_port():
    config = {"deployment": {"port": "8000"}}

    assert validate_port(config) == []
