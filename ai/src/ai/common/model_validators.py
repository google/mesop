def is_required_str(v: str) -> str:
  if v == "":
    raise ValueError("Field is required.")
  return v
