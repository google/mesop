"""
Formats the dataset for the fine-tuning process.
"""

import json
import os
from typing import Any

from llm_lib import REVISE_APP_BASE_PROMPT, SYSTEM_INSTRUCTION


def process_goldens():
  dataset: list[dict[str, Any]] = []
  outputs_dir = "goldens"

  for dir_name in os.listdir(outputs_dir):
    dir_path = os.path.join(outputs_dir, dir_name)
    if os.path.isdir(dir_path):
      prompt_path = os.path.join(dir_path, "prompt.txt")
      diff_path = os.path.join(dir_path, "diff.txt")

      with open(prompt_path) as prompt_file:
        prompt = prompt_file.read().strip()

      with open(diff_path) as diff_file:
        diff = diff_file.read().strip()

      code_path = os.path.join(dir_path, "source.py")
      if os.path.exists(code_path):
        with open(code_path) as code_file:
          code = code_file.read().strip()
      else:
        code = ""

      dataset.append(
        {
          "messages": [
            {
              "role": "system",
              "content": SYSTEM_INSTRUCTION,
            },
            {
              "role": "user",
              "content": REVISE_APP_BASE_PROMPT.replace(
                "<APP_CODE>", code
              ).replace("<APP_CHANGES>", prompt),
            },
            {
              "role": "assistant",
              "content": diff,
            },
          ],
        }
      )

  return dataset


if __name__ == "__main__":
  formatted_dataset = process_goldens()
  print(f"Processed {len(formatted_dataset)} samples.")
  # create gen dir if it doesn't exist
  os.makedirs("./gen", exist_ok=True)
  # Append each sample as a JSON object on a separate line to a file
  with open("./gen/formatted_dataset.jsonl", "w") as f:
    for sample in formatted_dataset:
      f.write(json.dumps(sample) + "\n")
