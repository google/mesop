import os

from ai.common.diff import create_udiff

GOLDENS_DIR = os.path.join(
  os.path.dirname(__file__), "..", "data", "golden_examples"
)


def generate_udiffs():
  for filename in os.listdir(GOLDENS_DIR):
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
    udiff = create_udiff(source, patched)
    print("udiff\n", udiff)
    with open(os.path.join(dir_path, "udiff.txt"), "w") as f:
      f.write(udiff)


if __name__ == "__main__":
  generate_udiffs()
