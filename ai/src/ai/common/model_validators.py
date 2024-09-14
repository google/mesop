def is_required_str(v: str) -> str:
  if v == "":
    raise ValueError("Field is required.")
  return v


def convert_empty_string_to_none(v):
  if isinstance(v, str) and v == "":
    return None
  return v
