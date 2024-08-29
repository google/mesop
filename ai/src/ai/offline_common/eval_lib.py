import base64
import concurrent.futures
import json
import os
import subprocess
from typing import Callable

import requests

SANDBOX_URL = "http://localhost:8080"


def run_eval(
  input_dir: str,
  file_stats: dict[str, list[str]],
  process_directory: Callable[[str], None],
):
  # Get all directories in the input_dir
  directories = [
    d
    for d in os.listdir(input_dir)
    if os.path.isdir(os.path.join(input_dir, d))
  ]

  with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
      executor.submit(process_directory, os.path.join(input_dir, directory))
      for directory in directories
    ]
    concurrent.futures.wait(futures)

  print(f"\nAll {len(directories)} directories processed successfully.")

  file_stats["error_count"] = len(file_stats["error"])  # type: ignore
  file_stats["success_count"] = len(directories) - file_stats["error_count"]  # type: ignore
  print_summary_statistics(file_stats)
  with open(os.path.join(input_dir, "stats.json"), "w") as f:
    json.dump(file_stats, f)


def print_summary_statistics(file_stats: dict[str, list[str]]):
  print("\nSummary Statistics:")
  print(f"# of files with errors: {file_stats['error_count']}")
  print(f"# of files without errors: {file_stats['success_count']}")
  if file_stats["error"]:
    print("\nFiles with errors:")
    for file in file_stats["error"]:
      print(f"- {file.replace('patched.py', 'error.txt')}")


def check_file_is_runnable(file_path: str, file_stats: dict[str, list[str]]):
  check_file_types(file_path, file_stats)
  check_file_is_executable(file_path, file_stats)


def check_file_types(file_path: str, file_stats: dict[str, list[str]]):
  try:
    subprocess.run(
      [
        "yarn",
        "pyright",
        file_path,
      ],
      capture_output=True,
      text=True,
      check=True,
    )
  except subprocess.CalledProcessError as e:
    file_stats["error"].append(file_path)
    error_output = e.stdout + e.stderr
    error_file_path = os.path.join(os.path.dirname(file_path), "error.txt")
    with open(error_file_path, "a") as f:
      f.write(f"Pyright error in {file_path}:\n")
      f.write(error_output)
      f.write("\n\n")
    print(
      f"Pyright error in {file_path}. Error details appended to {error_file_path}"
    )


def check_file_is_executable(file_path: str, file_stats: dict[str, list[str]]):
  with open(file_path) as f:
    code = f.read()
  result = requests.post(
    SANDBOX_URL + "/exec-py",
    data={"code": base64.b64encode(code.encode("utf-8"))},
  )
  if result.status_code != 200:
    file_stats["error"].append(file_path)
    error_file_path = os.path.join(os.path.dirname(file_path), "error.txt")
    with open(error_file_path, "a") as f:
      f.write(f"\nExecution error in {file_path}:\n")
      f.write(result.text)
      f.write("\n\n")
    print(
      f"Could not execute: {file_path}. Error details appended to {error_file_path}"
    )
