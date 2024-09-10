import json
import os

from ai.common.example import (
  ExampleInput,
  ExampleOutput,
  GoldenExample,
  golden_example_store,
)

OLD_GOLDENS_DIR = os.path.join(os.path.dirname(__file__), "..", "ft", "goldens")
NEW_GOLDENS_DIR = os.path.join(
  os.path.dirname(__file__), "..", "data", "golden_examples"
)


def migrate_goldens():
  for filename in os.listdir(OLD_GOLDENS_DIR):
    old_dir_path = os.path.join(OLD_GOLDENS_DIR, filename)
    if not os.path.isdir(old_dir_path):
      continue
    with open(os.path.join(old_dir_path, "diff.txt")) as f:
      diff = f.read()
    with open(os.path.join(old_dir_path, "prompt.txt")) as f:
      prompt = f.read()
    source = None
    if os.path.exists(os.path.join(old_dir_path, "source.py")):
      with open(os.path.join(old_dir_path, "source.py")) as f:
        source = f.read()
    with open(os.path.join(old_dir_path, "patched.py")) as f:
      patched = f.read()
    line_number = None
    if os.path.exists(os.path.join(old_dir_path, "metadata.json")):
      with open(os.path.join(old_dir_path, "metadata.json")) as f:
        metadata = json.load(f)
      line_number = metadata.get("line_number", None)
    golden_example = GoldenExample(
      id=filename,
      input=ExampleInput(
        prompt=prompt, input_code=source, line_number_target=line_number
      ),
      output=ExampleOutput(
        output_code=patched, raw_output=diff, output_type="diff"
      ),
      #   diff=diff,
      #   prompt=prompt,
      #   source=source,
      #   patched=patched,
      #   metadata=metadata,
    )
    golden_example_store.save(golden_example)


if __name__ == "__main__":
  migrate_goldens()
