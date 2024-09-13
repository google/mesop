import difflib
import os

from ai.common.diff import apply_udiff

GOLDENS_DIR = os.path.join(
  os.path.dirname(__file__), "..", "data", "golden_examples"
)


def verify_udiffs():
  for filename in os.listdir(GOLDENS_DIR):
    if (
      "Move_the_icon_buttons_below_the_bot_text_Muy5HQ_20240901000" in filename
    ):
      continue
    dir_path = os.path.join(GOLDENS_DIR, filename)
    if not os.path.isdir(dir_path):
      continue
    if not os.path.exists(os.path.join(dir_path, "input.py")):
      source = ""
    else:
      with open(os.path.join(dir_path, "input.py")) as f:
        source = f.read()
    with open(os.path.join(dir_path, "output.py")) as f:
      patched = f.read()
    with open(os.path.join(dir_path, "udiff.txt")) as f:
      udiff = f.read()
    result = apply_udiff(source, udiff)
    if result.has_error:
      raise Exception(result.result)
    if result.result.strip() != patched.strip():
      print("Output from udiff:")
      print(result.result)
      print("Expected:")
      print(patched)
      diff = difflib.unified_diff(
        patched.splitlines(keepends=True),
        result.result.splitlines(keepends=True),
        fromfile="Expected",
        tofile="Got",
        n=3,
      )
      print("".join(diff))
      raise Exception(f"Result does not match patched for {filename}")
    print(f"Verified {filename}")
  print("All verified")


if __name__ == "__main__":
  verify_udiffs()
