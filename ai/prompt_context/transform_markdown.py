"""
This script replaces mkdocs code and api placeholders with the actual code examples and
API docstrings and writes the modified output to a file.

This code needs to import mesop, so your terminal needs to have mesop imported via pip.
It does not seem to work when .cli.venv is loaded.
"""

import argparse
import inspect
import os

import mesop as me
import mesop.labs as mel
from mesop.features.theme import ThemeVar

DOCS_PATH = "../../docs/"
MARKDOWN_DOCS_CONTEXT_FILE = "markdown_docs_context.txt"
MARKDOWN_DOCS_BLOCKLIST_FILE = "markdown_docs_blocklist.txt"
OUTPUT_DIR = "../gen/extracted_markdown/"


def main():
  parser = argparse.ArgumentParser(
    prog="Transform Markdown",
    description="Transform markdown documents for prompt context.",
  )
  parser.add_argument("--use_cached_files_list", action="store_true")
  parser.add_argument("--cache_files_list", action="store_true")
  args = parser.parse_args()

  if args.use_cached_files_list and args.cache_files_list:
    print(
      "The flags --use_cached_files_list and --cache_files_list cannot be enabled at the same time"
    )
    return

  if args.use_cached_files_list:
    file_paths = read_file_paths_from_file(MARKDOWN_DOCS_CONTEXT_FILE)
  else:
    file_paths = get_file_paths_recursively(DOCS_PATH)

  if args.cache_files_list:
    write_file_paths_to_file(MARKDOWN_DOCS_CONTEXT_FILE, file_paths)

  filtered_file_paths = filter_file_paths(file_paths)
  process_documentation(filtered_file_paths)


def get_file_paths_recursively(directory):
  file_paths = []

  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".md"):
        file_path = os.path.relpath(os.path.join(root, file), directory)
        file_paths.append(directory + file_path)

  return file_paths


def write_file_paths_to_file(output_file, file_paths):
  with open(output_file, "w") as f:
    f.write("\n".join(file_paths).strip())


def read_file_paths_from_file(input_file):
  with open(input_file) as f:
    return list(filter(None, f.read().split("\n")))


def filter_file_paths(file_paths):
  blocklist = set(read_file_paths_from_file(MARKDOWN_DOCS_BLOCKLIST_FILE))
  return [file_path for file_path in file_paths if file_path not in blocklist]


def process_documentation(file_paths):
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

  total_char_count = 0
  processed_files = 0
  for file_path in file_paths:
    with open(file_path) as f:
      updated_lines = []
      for line in f.readlines():
        # Handle code snippet imports
        if line.startswith("--8<--"):
          with open(
            "../../" + line.removeprefix("--8<--").strip().replace('"', "")
          ) as f2:
            updated_lines.append(f2.read())
        # Handle doc strings
        elif line.startswith("::: "):
          try:
            symbol_name = line.removeprefix(":::").strip().split(".")[-1]
            if symbol_name == "ThemeVar":
              updated_lines.append("### ThemeVar \n")
              updated_lines.append("attr ThemeVar = " + str(ThemeVar) + "\n")
            else:
              if "mesop.labs." in line:
                symbol = getattr(mel, symbol_name)
              else:
                symbol = getattr(me, symbol_name)

              signature = inspect.signature(symbol)
              updated_lines.append("### " + symbol.__name__ + "\n")
              type_keyword = (
                "def" if "function" in str(symbol.__class__) else "class"
              )
              updated_lines.append("```python")
              updated_lines.append(
                type_keyword + " " + symbol.__name__ + str(signature) + ":"
              )
              updated_lines.append("  " + symbol.__doc__.strip())
              updated_lines.append("```\n")
          except Exception:
            print("Failed to process: " + line)
            updated_lines.append(line.strip())
        else:
          updated_lines.append(line.strip())

      file_contents = "\n".join(updated_lines).strip()
      char_count = len(file_contents)
      total_char_count += char_count
      processed_files += 1
      print(f"Processed {file_path}: {char_count:,} characters")

      with open(
        OUTPUT_DIR + file_path.replace("../../", "").replace("/", "_"), "w"
      ) as fw:
        fw.write(file_contents)

  print(f"Text extraction complete. Output written to {OUTPUT_DIR}")
  print(f"Total files processed: {processed_files}")
  print(f"Total characters extracted: {total_char_count:,}")


if __name__ == "__main__":
  main()
