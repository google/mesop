# Create a folder at out_dir + query (percent encoded)
import argparse
import os
import sys
import urllib.parse

from docs_index import blocking_query_engine
from llama_index.core.instrumentation import get_dispatcher
from llama_index.core.instrumentation.event_handlers import BaseEventHandler
from llama_index.core.instrumentation.events.llm import (
  LLMChatEndEvent,
  LLMCompletionEndEvent,
)


class ModelEventHandler(BaseEventHandler):
  @classmethod
  def class_name(cls) -> str:
    """Class name."""
    return "ModelEventHandler"

  def handle(self, event) -> None:
    """Logic for handling event."""
    if isinstance(event, LLMCompletionEndEvent):
      print(f"LLM Prompt length: {len(event.prompt)}")
      print(f"LLM Prompt CONTENT: {event.prompt}")
      print(f"LLM Completion: {event.response.text!s}")
    elif isinstance(event, LLMChatEndEvent):
      messages_str = "\n".join([str(x.content) for x in event.messages])
      print(f"LLM Input Messages RAW: {event.messages}")
      print(f"LLM Input Messages length: {len(messages_str)}")
      print(f"LLM Input Messages CONTENT: {messages_str}")
      print(f"LLM Response: {event.response.message.content!s}")

      # Create a folder for the query
      query_folder = os.path.join(args.out_dir, urllib.parse.quote(query))
      os.makedirs(query_folder, exist_ok=True)
      print(f"Created folder for query: {query_folder}")

      # Save the LLM input and output to files
      with open(os.path.join(query_folder, "input.txt"), "w") as f:
        f.write(messages_str)
      with open(os.path.join(query_folder, "output.txt"), "w") as f:
        f.write(str(event.response.message.content))


# root dispatcher
root_dispatcher = get_dispatcher()

# register event handler
root_dispatcher.add_event_handler(ModelEventHandler())

QUERIES = [
  "How can I reset an input component?",
  "Show me how to style a component",
  "Create a multi-page app",
  "Is it possible to create custom components?",
  "Implement authentication",
  "Deploy a Mesop app",
  "Optimize performance",
  "Can I use JavaScript libraries in Mesop?",
  "Stream UI updates from an LLM API",
  "Debug a Mesop application",
  "Is Mesop ready for production use?",
  "Create a mobile-friendly and responsive UI",
  "Handle asynchronous operations",
  "Implement dark mode",
  "Add tooltips to Mesop components",
  "Render a pandas DataFrame as a table",
  "Add charts",
  "Handle file uploads",
]

# QUERIES = [
#   "How do I test a Mesop application?",
#   "What components are available in Mesop?",
#   "How can I reset a text input field in Mesop?",
#   "Show me how to style a component in Mesop",
#   "Create a multi-page app using Mesop",
#   "Is it possible to create custom components in Mesop?",
#   "Implement authentication in a Mesop app",
#   "How do I call an API from a Mesop application?",
#   "What's the process for deploying a Mesop app?",
#   "Optimize performance in a Mesop application",
#   "Implement a datepicker in Mesop",
#   "Can I use JavaScript libraries with Mesop?",
#   "Implement real-time updates in a Mesop app",
#   "Stream UI updates from an LLM API in Mesop",
#   "Debug a Mesop application",
#   "Is Mesop ready for production use?",
#   "Implement form validation in Mesop",
#   "Create a mobile-friendly Mesop app",
#   "Handle asynchronous operations in Mesop",
#   "Implement dark mode in a Mesop application",
#   "Add keyboard shortcuts to a Mesop app",
#   "Implement drag and drop functionality in Mesop",
#   "Create an infinite scroll feature in Mesop",
#   "How to make a row of components in Mesop",
#   "Add tooltips to Mesop components",
#   "Render a pandas DataFrame in a Mesop app",
#   "Add charts to a Mesop application",
#   "Create a table component in Mesop",
#   "Handle file uploads in a Mesop app",
#   "Use command-line flags with a Mesop application",
#   "Create a clickable link in Mesop",
#   "Implement a download link in a Mesop app",
# ]


parser = argparse.ArgumentParser(
  description="Process queries and record model events."
)
parser.add_argument(
  "--out-dir", type=str, help="Output directory for recorded events"
)
args = parser.parse_args()

if args.out_dir:
  print(f"Output directory set to: {args.out_dir}")

  # Create the output directory if it doesn't exist
  os.makedirs(args.out_dir, exist_ok=True)
  print(f"Created output directory: {args.out_dir}")
else:
  print("No output directory specified. Exiting! Specify with --out-dir")
  sys.exit(1)


for query in QUERIES:
  blocking_query_engine.query(query)
