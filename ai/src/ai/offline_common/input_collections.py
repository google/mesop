from dataclasses import dataclass


@dataclass
class Input:
  prompt: str
  source_file: str | None = None


EASY_INPUTS = [
  Input(
    prompt="Make it more beautiful",
    source_file="./inputs/starter_kit.py",
  ),
  Input(
    prompt="Create an app that summarizes text from an input",
  ),
  Input(
    prompt="Create an app that allows you to change the tone of an input text using sliders",
  ),
  Input(
    prompt="Create an accordion",
  ),
  Input(
    prompt="Create a counter that increments by one",
  ),
  Input(
    prompt="Add a decrement button",
    source_file="./inputs/counter.py",
  ),
  Input(
    prompt="Swap the increment and decrement buttons",
    source_file="./inputs/counter_two_buttons.py",
  ),
  Input(
    prompt="Create a chat UI",
  ),
  Input(
    prompt="Create a row of cards",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Create a side-by-side layout",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Create a header footer layout",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Add an accordion",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Add a button",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Add a button and text input to collect feedback",
    source_file="./inputs/simple.py",
  ),
  Input(
    prompt="Turn it into a row",
    source_file="./inputs/before_row.py",
  ),
]

HARD_INPUTS = [
  Input(
    prompt="Create a text to image UI",
  ),
  Input(
    prompt="Create a chat UI",
  ),
  Input(
    prompt="Implement a tone adjustment feature (formal, casual, persuasive)",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Allow the user to upload an image and chat with it",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Show a row of example prompts that users can click on",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add a button and text input to collect feedback for each response",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add chips to suggest follow-up topics after the last response",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add the ability to edit the last user message",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Make it look more beautiful",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add a 'summarize this conversation' button",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add a way to save a conversation",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Show the outputs of two models side-by-side",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Add a way to add system instructions",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Displays citations in the responses",
    source_file="./inputs/chat.py",
  ),
  Input(
    prompt="Create a text summarization interface",
  ),
  Input(
    prompt="Create an LLM playground",
  ),
]
