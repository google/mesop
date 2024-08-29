import argparse
import os
import urllib.parse

from ai.common.llm_lib import apply_patch
from ai.offline_common.eval_lib import check_file_is_runnable, run_eval

file_stats: dict[str, list[str]] = {
  "error": [],
  "success": [],
}


def process_directory(directory_path: str):
  print(f"Processing directory: {directory_path}")
  error_file_path = os.path.join(directory_path, "error.txt")
  # Remove error files from a previous run
  if os.path.exists(error_file_path):
    os.remove(error_file_path)

  diff_file_path = os.path.join(directory_path, "diff.txt")

  if not os.path.exists(diff_file_path):
    print(f"Error: diff.txt not found in {directory_path}")
    return

  with open(diff_file_path) as f:
    patch = f.read()

  dirname = os.path.basename(directory_path)
  segments = dirname.split("__")
  assert (
    len(segments) == 2
  ), f"Expected dirname to have two segments, but got: {dirname}"

  if segments[1] == "no_source":
    content = ""
  else:
    input_source_path = os.path.join(
      "src/ai/offline_common", urllib.parse.unquote(segments[1])
    )
    # Read the original content if it's not a "no_source" file
    with open(input_source_path) as f:
      content = f.read()

  patch_result = apply_patch(original_code=content, patch=patch)

  if patch_result.has_error:
    with open(os.path.join(directory_path, "error.txt"), "w") as f:
      f.write(patch_result.result)
    print("Patch has error:", patch_result.result)
    file_stats["error"].append(diff_file_path)
  else:
    output_file = os.path.join(directory_path, "patched.py")
    with open(output_file, "w") as f:
      f.write(patch_result.result)

    print(f"Patched content written to: {output_file}")
    check_file_is_runnable(os.path.abspath(output_file), file_stats)


def parse_arguments():
  parser = argparse.ArgumentParser(
    description="Evaluate patches for Mesop app."
  )
  parser.add_argument(
    "--model", type=str, required=True, help="Specify the model to use"
  )
  parser.add_argument(
    "--run_name", type=str, required=True, help="Specify a name for this run"
  )
  return parser.parse_args()


def main():
  args = parse_arguments()

  input_dir = os.path.join("outputs", args.model, args.run_name)

  if not os.path.exists(input_dir):
    print(f"Error: Directory not found: {input_dir}")
    return

  print(f"Processing files in: {input_dir}")
  print(f"Using model: {args.model}")
  print(f"Run name: {args.run_name}")
  run_eval(input_dir, file_stats, process_directory)


if __name__ == "__main__":
  main()
