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
    # producer = producer_store.get(producer_id)
    # print("create_golden_dataset", producer)
    # return "not yet implemented"
