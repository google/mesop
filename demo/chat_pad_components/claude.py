import anthropic

from chat_pad_components.data_model import ChatMessage

client = anthropic.Anthropic(
  # defaults to os.environ.get("ANTHROPIC_API_KEY")
  #   api_key="my_api_key",
)


def call_claude_sonnet(input: str, history: list[ChatMessage]):
  messages = [
    {
      "role": "assistant" if message.role == "model" else message.role,
      "content": message.content,
    }
    for message in history
  ] + [{"role": "user", "content": input}]
  with client.messages.stream(
    max_tokens=1024,
    messages=messages,
    model="claude-3-5-sonnet-20240620",
  ) as stream:
    for text in stream.text_stream:
      yield text
