PROMPT_INSTRUCTIONS = """

FOLLOW EACH OF THESE INSTRUCTIONS VERY CAREFULLY:
- Do NOT set a default value for fields in State (or any class annotated with stateclass).
  - ESPECIALLY, DO NOT SET A DEFAULT VALUE FOR A MUTABLE TYPE LIKE LIST.
- Prefer using on_blur over on_input for the input component.
- You should cite sources.
- Make your responses succinct.
- DO NOT USE `mesop.run()` or `me.run()` in the code. It does not exist!
- ALWAYS ASSUME THE USER WANTS CODE FOR MESOP (do NOT return code for HTML/CSS/React/etc)
"""

# The GitHub discussions seems too noisy and adds a lot of tokens
# (e.g. release notes, back and forth with answering questions)
# so it's not being used for now.
# with open("gen/prompt_context/discussions.txt", encoding="utf-8") as file:
#   discussions = file.read()

with open("gen/prompt_context/api_docs.txt", encoding="utf-8") as file:
  api_docs = file.read()

SYSTEM_PROMPT = api_docs + PROMPT_INSTRUCTIONS
print(SYSTEM_PROMPT)
