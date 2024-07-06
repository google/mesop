import google.generativeai as genai
import os
from chat_pad_components.data_model import ChatMessage

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def send_prompt(prompt: str, history: list[ChatMessage]):
  chat_session = model.start_chat(
    history=[
      {"role": message.role, "parts": [message.content]} for message in history
    ]
  )

  return chat_session.send_message(prompt, stream=True)


# pass
