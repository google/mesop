import base64
import concurrent.futures
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Literal

import requests
from pydantic import BaseModel

from ai.common.entity_store import EntityStore, get_data_path
from ai.common.example import (
  EvaluatedExample,
  EvaluatedExampleOutput,
  ExampleOutput,
  ExpectedExample,
  ExpectResult,
  expected_example_store,
)
from ai.common.executor import ProducerExecutor

SANDBOX_URL = "http://localhost:8080"


class EvalOutcome(BaseModel):
  examples_run: int
  examples_succeeded: int
  score: float  # sum of scores across expect_results in examples


class Eval(BaseModel):
  id: str
  producer_id: str
  # use a seed to make the eval deterministic and enable caching.
  seed: int = 0
  state: Literal["pending", "running", "complete", "failed"] = "pending"
  eval_outcome: EvalOutcome | None = None


eval_store = EntityStore(Eval, dirname="evals")


def get_eval_example(eval_id: str, example_id: str) -> EvaluatedExample:
  eval_path = get_data_path(os.path.join("evals", eval_id))
  if not os.path.exists(eval_path):
    raise ValueError(f"Eval {eval_id} example {example_id} not found")
  with open(os.path.join(eval_path, example_id, "evaluated_example.json")) as f:
    evaluated_example = EvaluatedExample.model_validate_json(f.read())
  with open(os.path.join(eval_path, example_id, "output.txt")) as f:
    evaluated_example.outputs[0].output.raw_output = f.read()
  if os.path.exists(os.path.join(eval_path, example_id, "patched.py")):
    with open(os.path.join(eval_path, example_id, "patched.py")) as f:
      evaluated_example.outputs[0].output.output_code = f.read()
  return evaluated_example


def get_eval_examples(eval_id: str) -> list[EvaluatedExample]:
  eval_path = get_data_path(os.path.join("evals", eval_id))
  if not os.path.exists(eval_path):
    return []
  examples: list[EvaluatedExample] = []
  for file in os.listdir(eval_path):
    json_path = os.path.join(eval_path, file, "evaluated_example.json")
    if os.path.exists(json_path):
      with open(json_path) as f:
        examples.append(EvaluatedExample.model_validate_json(f.read()))
  return examples


class EvalRunner:
  def __init__(self, eval: Eval):
    self.eval = eval
    self.producer_executor = ProducerExecutor(self.eval.producer_id)
    self.eval_path = get_data_path(os.path.join("evals", self.eval.id))

  def run(self):
    os.makedirs(self.eval_path, exist_ok=True)

    examples = expected_example_store.get_all()
    eval_outcome = EvalOutcome(examples_run=0, examples_succeeded=0, score=0)

    try:
      with ThreadPoolExecutor() as executor:
        future_to_example = {
          executor.submit(self.eval_example, example): example
          for example in examples
        }
        for future in concurrent.futures.as_completed(future_to_example):
          evaluated_example = future.result()
          eval_outcome.examples_run += 1
          for result in evaluated_example.outputs[0].expect_results:
            eval_outcome.score += result.score
          if all(
            result.score == 1
            for result in evaluated_example.outputs[0].expect_results
          ):
            eval_outcome.examples_succeeded += 1
          print("---")
          print("Proessed: ", evaluated_example.expected.id)
          print(
            f"Examples succeeded: {eval_outcome.examples_succeeded}/{len(examples)}"
          )
          print("---")
    except Exception as e:
      self.eval.state = "failed"
      eval_store.save(self.eval, overwrite=True)
      raise e

    self.eval.state = "complete"
    self.eval.eval_outcome = eval_outcome
    eval_store.save(self.eval, overwrite=True)

  def eval_example(self, example: ExpectedExample) -> EvaluatedExample:
    example_path = os.path.join(self.eval_path, example.id)
    os.makedirs(example_path)

    start_time = time.time()
    output = self.producer_executor.execute(example.input, seed=self.eval.seed)
    end_time = time.time()
    time_elapsed = end_time - start_time
    with open(os.path.join(example_path, "output.txt"), "w") as f:
      f.write(output)

    evaluated_example_output = EvaluatedExampleOutput(
      time_spent_secs=time_elapsed,
      tokens=int(len(output) / 4),  # rough estimate
      output=ExampleOutput(
        output_type=self.producer_executor.producer.output_format,
      ),
      expect_results=[],
    )

    patched_code = self.producer_executor.transform_output(
      input_code=example.input.input_code or "", output=output
    )
    evaluated_example_output.expect_results.append(
      ExpectResult(
        name="patchable",
        score=0 if patched_code.has_error else 1,
        message=patched_code.result if patched_code.has_error else "Success",
      )
    )
    if not patched_code.has_error:
      patched_code_path = os.path.join(example_path, "patched.py")
      with open(patched_code_path, "w") as f:
        f.write(patched_code.result)

      self.check_executable(evaluated_example_output, patched_code_path)
      self.check_type_checkable(evaluated_example_output, patched_code_path)
    evaluated_example = EvaluatedExample(
      expected=example,
      outputs=[evaluated_example_output],
    )

    with open(os.path.join(example_path, "evaluated_example.json"), "w") as f:
      f.write(evaluated_example.model_dump_json(indent=4))
    return evaluated_example

  def check_type_checkable(
    self,
    evaluated_example_output: EvaluatedExampleOutput,
    patched_code_path: str,
  ):
    try:
      subprocess.run(
        [
          "yarn",
          "pyright",
          patched_code_path,
        ],
        capture_output=True,
        text=True,
        check=True,
      )
      evaluated_example_output.expect_results.append(
        ExpectResult(
          name="type_checkable",
          score=1,
          message="Success",
        )
      )
    except subprocess.CalledProcessError as e:
      evaluated_example_output.expect_results.append(
        ExpectResult(
          name="type_checkable", score=0, message=e.stdout + e.stderr
        )
      )

  def check_executable(
    self,
    evaluated_example_output: EvaluatedExampleOutput,
    patched_code_path: str,
  ):
    with open(patched_code_path) as f:
      code = f.read()
    result = requests.post(
      SANDBOX_URL + "/exec-py",
      data={"code": base64.b64encode(code.encode("utf-8"))},
    )
    if result.status_code == 200:
      evaluated_example_output.expect_results.append(
        ExpectResult(
          name="executable",
          score=1,
          message="Success",
        )
      )
    else:
      evaluated_example_output.expect_results.append(
        ExpectResult(
          name="executable",
          score=0,
          message=result.text,
        )
      )
