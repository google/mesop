PROMPT_INSTRUCTIONS = """
- Do NOT set a default value for fields in State (or any class annotated with stateclass).
- Prefer using on_blur over on_input for the input component.
- You should cite sources.
- Make your responses succinct.
"""

with open("gen/prompt_context/discussions.txt", encoding="utf-8") as file:
  discussions = file.read()

with open("gen/prompt_context/api_docs.txt", encoding="utf-8") as file:
  api_docs = file.read()

SYSTEM_PROMPT = api_docs + discussions + PROMPT_INSTRUCTIONS
print(SYSTEM_PROMPT)
