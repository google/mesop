import json
import os

from ai.common.entity_store import get_data_path
from ai.common.example import golden_example_store
from ai.common.executor import ProducerExecutor


def create_golden_dataset(*, producer_id: str, dataset_name: str) -> str:
  #  examples: list[GoldenExample],
  golden_dataset_path = os.path.join(
    get_data_path("golden_datasets"), f"{dataset_name}.jsonl"
  )
  with open(golden_dataset_path, "w") as f:
    examples = golden_example_store.get_all()
    producer_executor = ProducerExecutor(producer_id)
    for example in examples:
      messages = producer_executor.get_provider_executor().format_messages(
        example.input
      )
      if example.output.udiff_output is None:
        raise ValueError("udiff_output is required", example)
      messages.append(
        {
          "role": "assistant",
          "content": example.output.udiff_output,
        }
      )
      f.write(json.dumps({"messages": messages}) + "\n")
    print("created golden dataset", golden_dataset_path)
    convert_openai_format_to_llama3_format(
      golden_dataset_path,
      golden_dataset_path.replace(".jsonl", "_llama3.jsonl"),
    )
    return golden_dataset_path


def convert_openai_format_to_llama3_format(input_file: str, output_file: str):
  with open(input_file) as in_f, open(output_file, "w") as out_f:
    for line in in_f:
      data = json.loads(line.strip())
      output = "<|begin_of_text|>"

      for message in data["messages"]:
        role, content = message["role"], message["content"]
        output += (
          f"<|start_header_id|>{role}<|end_header_id|> {content}<|eot_id|>"
        )

      out_f.write(json.dumps({"text": output}) + "\n")
