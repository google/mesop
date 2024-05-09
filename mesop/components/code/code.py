from mesop.component_helpers import component
from mesop.components.markdown.markdown import markdown


@component
def code(code: str = "", *, language: str = "python"):
  """
  Creates a code component which displays code with syntax highlighting.
  """
  markdown("``` " + language + "\n" + code + "\n" + "```")
