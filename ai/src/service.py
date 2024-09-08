import json
import os
import secrets
import urllib.parse
from dataclasses import asdict, dataclass
from datetime import datetime
from os import getenv

from flask import Flask, Response, request, stream_with_context

from ai.common.llm_lib import adjust_mesop_app_stream, apply_patch

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
  diff = data.get("diff")

  if not prompt or not before_code or not diff:
    return Response("Invalid request", status=400)

  line_number = data.get("lineNumber")
  if line_number is not None:
    metadata = InteractionMetadata(line_number=line_number)
  else:
    metadata = None
  folder_name = generate_folder_name(prompt)
  base_path = "ft/goldens"
  folder_path = os.path.join(base_path, folder_name)

  os.makedirs(folder_path, exist_ok=True)

  with open(os.path.join(folder_path, "prompt.txt"), "w") as f:
    f.write(prompt)
  with open(os.path.join(folder_path, "source.py"), "w") as f:
    f.write(before_code)
  with open(os.path.join(folder_path, "diff.txt"), "w") as f:
    f.write(diff)
  if metadata is not None:
    with open(os.path.join(folder_path, "metadata.json"), "w") as f:
      json.dump(asdict(metadata), f)

  return {"folder": folder_name}


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
    stream = adjust_mesop_app_stream(
      code=code,
      user_input=prompt,
      line_number=line_number,
    )
    diff = ""
    for chunk in stream:
      if chunk:
        diff += chunk
        yield f"data: {json.dumps({'type': 'progress', 'data': chunk})}\n\n"

    result = apply_patch(code, diff)
    if result.has_error:
      yield f"data: {json.dumps({'type': 'error', 'error': result.result})}\n\n"
      return

    yield f"data: {json.dumps({'type': 'end', 'code': result.result, 'diff': diff})}\n\n"

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
