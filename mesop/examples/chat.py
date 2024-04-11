import random
import time

import mesop as me
import mesop.labs as mel


@me.page(path="/chat", title="Lorem Ipsum Chat")
def page():
  mel.chat(
    lorem_ipsum_chat, title="Lorem Ipsum Chat", bot_user="Lorem Ipsum Bot"
  )


def lorem_ipsum_chat(input: str, history: list[mel.ChatMessage]):
  lines = [
    (
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
      "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    ),
    "Laoreet sit amet cursus sit amet dictum sit amet.",
    "At lectus urna duis convallis.",
    "A pellentesque sit amet porttitor eget.",
    "Mauris nunc congue nisi vitae suscipit tellus mauris a diam.",
    "Aliquet lectus proin nibh nisl condimentum id.",
    "Integer malesuada nunc vel risus commodo viverra maecenas accumsan.",
    "Tempor id eu nisl nunc mi.",
    "Id consectetur purus ut faucibus pulvinar.",
    "Mauris pharetra et ultrices neque ornare.",
    "Facilisis magna etiam tempor orci.",
    "Mauris pharetra et ultrices neque.",
    "Sit amet facilisis magna etiam tempor orci.",
    "Amet consectetur adipiscing elit pellentesque habitant morbi tristique.",
    "Egestas erat imperdiet sed euismod.",
    "Tincidunt praesent semper feugiat nibh sed pulvinar proin gravida.",
    "Habitant morbi tristique senectus et netus et malesuada.",
  ]
  for line in random.sample(lines, random.randint(3, len(lines) - 1)):
    time.sleep(0.3)
    yield line + " "
