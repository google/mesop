from mesop.runtime import runtime
from mesop.server.wsgi_app import create_app


def test_wsgi_app_prod_mode():
  app = create_app(prod_mode=True)
  assert app is not None
  assert runtime().debug_mode is False


def test_wsgi_app_debug_mode():
  app = create_app(prod_mode=False)
  assert app is not None
  assert runtime().debug_mode is True


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
