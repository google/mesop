import io


# Store this class in a separate file so we can more easily reference
# in dataclass utils.
class UploadedFile(io.BytesIO):
  """Uploaded file contents and metadata."""

  def __init__(
    self,
    contents: bytes = b"",
    *,
    name: str = "",
    size: int = 0,
    mime_type: str = "",
  ):
    super().__init__(contents)
    self._name = name
    self._size = size
    self._mime_type = mime_type

  @property
  def name(self):
    return self._name

  @property
  def size(self):
    return self._size

  @property
  def mime_type(self):
    return self._mime_type

  def __eq__(self, other):
    if isinstance(other, UploadedFile):
      return (self.getvalue(), self.name, self.size, self.mime_type) == (
        other.getvalue(),
        other.name,
        other.size,
        other.mime_type,
      )
    return False
