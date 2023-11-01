import optic.hello as hello


def test_hello_world():
    assert hello.greet() == "hello"


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
