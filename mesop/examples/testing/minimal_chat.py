import mesop as me
import mesop.labs as mel


@me.page(path="/testing/minimal_chat", title="Lorem Ipsum Chat")
def page():
  mel.chat(transform, title="Lorem Ipsum Chat", bot_user="Lorem Ipsum Bot")


def transform(input: str, history: list[mel.ChatMessage]):
  yield "Echo: "
  yield input
