"""
Formats the golden dataset for the fine-tuning process.
"""

import argparse
import csv
import json
import os
from datetime import datetime
from typing import Any

from ai.common.llm_lib import (
  MakeDefaultMessageFormatter,
  MakeMessageFormatterShorterUserMsg,
)

# TODO: Allow this to be configurable
FINE_TUNING_CUTOFF = datetime(2024, 8, 2, 0, 0)


def process_goldens(
  skip_fine_tuned_goldens: bool = False, gemini_format: bool = False
):
  dataset: list[dict[str, Any]] = []
  outputs_dir = "ft/goldens"

  for dir_name in os.listdir(outputs_dir):
    dir_path = os.path.join(outputs_dir, dir_name)
    if os.path.isdir(dir_path):
      prompt_path = os.path.join(dir_path, "prompt.txt")
      diff_path = os.path.join(dir_path, "diff.txt")
      line_number: int | None = None
      meta_path = os.path.join(dir_path, "metadata.json")

      _, timestamp = os.path.basename(dir_path).rsplit("_", 1)
      creation_date = datetime.strptime(timestamp, "%Y%m%d%H%M")

      if skip_fine_tuned_goldens and creation_date < FINE_TUNING_CUTOFF:
        continue

      if os.path.exists(meta_path):
        with open(meta_path) as meta_file:
          meta = json.load(meta_file)
          line_number = meta.get("line_number")
          print(f"line_number: {line_number}")

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

      if skip_fine_tuned_goldens or gemini_format:
        formatter = MakeMessageFormatterShorterUserMsg()
      else:
        formatter = MakeDefaultMessageFormatter()

      dataset.append(
        {
          "messages": [
            *formatter.format_messages(code, prompt, line_number),
            {
              "role": "assistant",
              "content": diff,
            },
          ],
        }
      )

  return dataset


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--skip_fine_tuned_goldens",
    action="store_true",
    help="Generates a formatted dataset with goldens that have not been fine tuned.",
  )
  parser.add_argument(
    "--gemini_format",
    action="store_true",
    help="Generates a Gemini formatted dataset.",
  )
  args = parser.parse_args()

  formatted_dataset = process_goldens(
    args.skip_fine_tuned_goldens, args.gemini_format
  )
  print(f"Processed {len(formatted_dataset)} samples.")
  # create gen dir if it doesn't exist
  os.makedirs("ft/gen", exist_ok=True)

  if args.skip_fine_tuned_goldens:
    if args.gemini_format:
      full_path = os.path.join(
        "ft/gen/gemini_formatted_dataset_for_prompting.csv"
      )
    else:
      full_path = os.path.join("ft/gen/formatted_dataset_for_prompting.jsonl")
  else:
    if args.gemini_format:
      full_path = os.path.join("ft/gen/gemini_formatted_dataset.csv")
    else:
      full_path = os.path.join("ft/gen/formatted_dataset.jsonl")

  if args.gemini_format:
    with open(full_path, "w") as f:
      writer = csv.writer(f)
      writer.writerow(["input:", "output:"])
      for sample in formatted_dataset:
        writer.writerow(
          [sample["messages"][1]["content"], sample["messages"][2]["content"]]
        )
  else:
    # Append each sample as a JSON object on a separate line to a file
    with open(full_path, "w") as f:
      for sample in formatted_dataset:
        f.write(json.dumps(sample) + "\n")

  # Print absolute path of file
  print(f"File created at: {full_path}")
