import gzip
import tempfile
from io import BytesIO

from flask import Flask

from mesop.server.static_file_serving import gzip_cache, send_file_compressed


# Putting this test first because it's making sure the cache is empty.
# Note: the cache is a static variable.
def test_send_file_compressed_do_not_cache():
  app = Flask(__name__)
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    file_content = b"abc"
    tmp_file.write(file_content)
    tmp_file_path = tmp_file.name

  with app.test_request_context():
    send_file_compressed(tmp_file_path, disable_gzip_cache=True)
    # Check that cache is still empty
    assert len(gzip_cache) == 0


def test_send_file_compressed_uncached_request():
  app = Flask(__name__)
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    file_content = b"abc"
    tmp_file.write(file_content)
    tmp_file_path = tmp_file.name

  with app.test_request_context():
    response = send_file_compressed(tmp_file_path, disable_gzip_cache=False)

    assert response.headers["Content-Encoding"] == "gzip"
    assert response.direct_passthrough is False
    assert int(response.headers["Content-Length"]) == len(response.get_data())

    # Check if the ungzipped data is correct
    with gzip.GzipFile(fileobj=BytesIO(response.get_data()), mode="rb") as f:
      ungzipped_data = f.read()
      assert ungzipped_data == file_content

    # Check that cache is properly stored
    assert len(gzip_cache) == 1
    assert gzip_cache[tmp_file_path] == response.get_data()


def test_send_file_compressed_cached_request():
  app = Flask(__name__)
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    tmp_file.write(b"")
    tmp_file_path = tmp_file.name

  cached_bytes = b"test_data"
  gzip_buffer = BytesIO()
  with gzip.GzipFile(
    mode="wb", fileobj=gzip_buffer, compresslevel=6
  ) as gzip_file:
    gzip_file.write(cached_bytes)
  gzip_buffer.seek(0)
  gzip_cache[tmp_file_path] = gzip_buffer.getvalue()
  with app.test_request_context():
    response = send_file_compressed(tmp_file_path, disable_gzip_cache=False)

    assert response.headers["Content-Encoding"] == "gzip"
    assert response.direct_passthrough is False
    assert int(response.headers["Content-Length"]) == len(response.get_data())

    # Check that the cached bytes is returned
    with gzip.GzipFile(fileobj=BytesIO(response.get_data()), mode="rb") as f:
      ungzipped_data = f.read()
      assert ungzipped_data == cached_bytes


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
