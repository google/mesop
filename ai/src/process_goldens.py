import os

from ai.common.llm_lib import apply_patch
from ai.offline_common.eval_lib import check_file_is_runnable, run_eval

file_stats: dict[str, list[str]] = {
  "error": [],
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

  content = ""
  SOURCE_PY_PATH = os.path.join(directory_path, "source.py")
  if os.path.exists(SOURCE_PY_PATH):
    with open(SOURCE_PY_PATH) as f:
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


def main():
  input_dir = os.path.join("ft/goldens")

  if not os.path.exists(input_dir):
    print(f"Error: Directory not found: {input_dir}")
    return

  print(f"Processing files in: {input_dir}")
  run_eval(input_dir, file_stats, process_directory)


if __name__ == "__main__":
  main()
