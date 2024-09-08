import argparse
import json
import multiprocessing
import os
import time
from functools import wraps
from typing import Any, Callable
from urllib.parse import quote

from ai.common.llm_lib import (
  MakeDefaultPrompt,
  MakeDefaultSystemInstruction,
  adjust_mesop_app_blocking,
)
from ai.offline_common.input_collections import EASY_INPUTS, Input

SYSTEM_INSTRUCTION = MakeDefaultSystemInstruction()
PROMPT = MakeDefaultPrompt()


def parse_arguments():
  parser = argparse.ArgumentParser(
    description="Process inputs for Mesop app adjustment."
  )
  parser.add_argument(
    "--model", type=str, required=True, help="Specify the model to use"
  )
  parser.add_argument(
    "--run_name", type=str, required=True, help="Specify a name for this run"
  )
  parser.add_argument(
    "--num_inputs",
    type=int,
    default=None,
    help="Number of inputs to process (default: all)",
  )
  parser.add_argument(
    "--workers",
    type=int,
    default=None,
    help="Number of worker processes in the pool (default: number of CPU cores)",
  )
  return parser.parse_args()


def retry_with_specific_waits() -> Callable[..., Any]:
  wait_times = [10, 30, 60]

  def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
      for attempt, wait_time in enumerate(wait_times, start=1):
        try:
          return func(*args, **kwargs)
        except Exception as e:
          if attempt == len(wait_times):
            print(f"Max retries reached. Last error: {e!s}")
            raise
          print(
            f"Error: {e!s}. Retrying in {wait_time} seconds... (Attempt {attempt}/{len(wait_times)})"
          )
          time.sleep(wait_time)

    return wrapper

  return decorator


@retry_with_specific_waits()
def process_input(
  input: Input, i: int, total: int, output_dir: str, model: str
):
  start_time = time.time()
  print(f"\nProcessing input {i}/{total}: {input.prompt}")

  if input.source_file:
    full_path = os.path.abspath(
      os.path.join("src/ai/offline_common", input.source_file)
    )
    print(f"Reading source file: {full_path}")
    with open(full_path) as f:
      code = f.read()
  else:
    print("No source file provided.")
    code = ""

  output = adjust_mesop_app_blocking(
    user_input=input.prompt, code=code, model=model
  )

  # Create a filename based on the prompt and source_file
  source_file_part = (
    quote(input.source_file, safe="") if input.source_file else "no_source"
  )
  output_subdir = os.path.join(
    output_dir,
    f"{quote(input.prompt, safe='')}__{source_file_part}",
  )
  os.makedirs(output_subdir, exist_ok=True)
  filepath = os.path.join(output_subdir, "diff.txt")

  print(f"Writing output to: {filepath}")
  with open(filepath, "w") as f:
    f.write(output)

  print(f"Completed processing input {i}")
  end_time = time.time()
  processing_time = end_time - start_time
  return input.prompt, processing_time


def main():
  args = parse_arguments()

  output_dir = os.path.join("outputs", args.model, args.run_name)
  os.makedirs(output_dir, exist_ok=False)

  # Write system instructions
  with open(os.path.join(output_dir, "prompt.txt"), "w") as f:
    f.write(PROMPT)

  # Write system instructions
  with open(os.path.join(output_dir, "system_instructions.txt"), "w") as f:
    f.write(SYSTEM_INSTRUCTION)

  inputs = EASY_INPUTS

  if args.num_inputs is not None:
    inputs_to_process = inputs[: args.num_inputs]
  else:
    inputs_to_process = inputs

  print(f"Processing {len(inputs_to_process)} inputs...")
  print(f"Using model: {args.model}")
  print(f"Run name: {args.run_name}")

  # Create a pool of worker processes with the specified number of workers
  with multiprocessing.Pool(processes=args.workers) as pool:
    # Use starmap to pass multiple arguments to the process_input function
    results = pool.starmap(
      process_input,
      [
        (input, i, len(inputs_to_process), output_dir, args.model)
        for i, input in enumerate(inputs_to_process)
      ],
    )

    performance_data = {}
    for prompt, processing_time in results:
      performance_data[prompt] = processing_time

  print(f"Performance data: {performance_data}")
  # Save performance data to perf.json
  perf_filepath = os.path.join(output_dir, "perf.json")
  with open(perf_filepath, "w") as f:
    json.dump(performance_data, f, indent=2)

  print(f"\nPerformance data saved to: {perf_filepath}")
  print("\nAll inputs processed successfully.")


if __name__ == "__main__":
  main()
