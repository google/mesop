import json
import secrets
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from os import getenv

from flask import Flask, Response, request, stream_with_context

from ai.common.example import (
  ExampleInput,
  ExampleOutput,
  GoldenExample,
  golden_example_store,
)
from ai.common.executor import (
  ProducerExecutor,
)

app = Flask(__name__)


@dataclass
class InteractionMetadata:
  line_number: int | None


@app.route("/save-interaction", methods=["POST"])
def save_interaction_endpoint() -> Response | dict[str, str]:
  data = request.json
  assert data is not None
  prompt = data.get("prompt")
  before_code = data.get("beforeCode")
  after_code = data.get("afterCode")
  diff = data.get("diff")

  if not prompt or not before_code or not diff:
    return Response("Invalid request", status=400)

  line_number = data.get("lineNumber")

  folder_name = generate_folder_name(prompt)
  golden_example = GoldenExample(
    id=folder_name,
    input=ExampleInput(
      prompt=prompt, input_code=before_code, line_number_target=line_number
    ),
    output=ExampleOutput(
      output_code=after_code, raw_output=diff, output_type="udiff"
    ),
  )
  golden_example_store.save(golden_example)

  return {"folder": folder_name}


DEFAULT_PRODUCER_ID = "gpt4o-mini-udiff-ft"


@app.route("/adjust-mesop-app", methods=["POST"])
def adjust_mesop_app_endpoint():
  data = request.json
  assert data is not None
  code = data.get("code")
  prompt = data.get("prompt")
  line_number = data.get("lineNumber")

  if not code or not prompt:
    return Response("Both 'code' and 'prompt' are required", status=400)

  def generate():
    executor = ProducerExecutor(DEFAULT_PRODUCER_ID)
    stream = executor.execute_stream(
      ExampleInput(
        input_code=code, prompt=prompt, line_number_target=line_number
      )
    )

    acc = ""
    for chunk in stream:
      acc += chunk
      yield f"data: {json.dumps({'type': 'progress', 'data': chunk})}\n\n"

    result = executor.transform_output(input_code=code, output=acc)
    if result.has_error:
      yield f"data: {json.dumps({'type': 'error', 'error': result.result})}\n\n"
      return

    yield f"data: {json.dumps({'type': 'end', 'code': result.result, 'diff': acc})}\n\n"

  return Response(
    stream_with_context(generate()), content_type="text/event-stream"
  )


def generate_folder_name(prompt: str) -> str:
  prompt = prompt.replace(
    " ", "_"
  )  # Replace spaces with underscores to avoid %20
  # Generate a unique 4-character suffix to avoid naming collisions
  suffix = secrets.token_urlsafe(4)
  # Generate timestamp to help with determining which goldens have been added to the
  # finetuned models.
  timestamp = datetime.now().strftime("%Y%m%d%H%M")
  cleaned_prompt = urllib.parse.quote(prompt)[:50]

  return f"{cleaned_prompt}_{suffix}_{timestamp}"


if __name__ == "__main__":
  port = int(getenv("PORT", 43234))
  app.run(port=port)
