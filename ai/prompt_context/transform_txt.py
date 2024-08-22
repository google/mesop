"""
Turns the extracted text into a format ideal for LLM consumption.

Pre-requisite:

Run `python transform_html.py` first to extract the text from the HTML files.
"""

import os
import time

import google.generativeai as genai

# Note: this prompt does not work well for every file
# in particular, it omits too much information from the style API.
# I use this to cleanup the style doc:
# "Clean up the formatting for the following Python docs to make it easier for an LLM to understand:"
PROMPT = """Here's a prompt to teach an LLM to extract useful information from a doc page and create a condensed prompt context:

Extract key information from the given documentation page to create a condensed yet comprehensive prompt context. Focus on:

1. Core concepts and definitions
2. API signatures and parameters
3. Important code snippets and examples
4. Key usage patterns and best practices
5. Crucial warnings or limitations

Omit:
- Redundant explanations
- Verbose examples (keep only the most illustrative ones)
- Introductory or concluding paragraphs that don't add technical value

Format the output as follows:

```
[COMPONENT_NAME]
Brief description (1-2 sentences max)

Key Concepts:
• Concept 1
• Concept 2

API:
function_name(param1: Type, param2: Type) -> ReturnType
  Brief description

Code Example:
```python
# Minimal working example
```

Usage Notes:
- Important usage note 1
- Important usage note 2

Warnings:
! Critical warning or limitation
```

Prioritize accuracy and completeness while minimizing token usage. Preserve code indentation and formatting for readability.
"""


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # type: ignore

model = genai.GenerativeModel("gemini-1.5-flash-latest")


def generate_refined_text(content: str):
  max_retries = 2
  backoff_factor = 2
  for attempt in range(max_retries):
    try:
      response = model.generate_content(PROMPT + "\n\n" + content)  # type: ignore
      return response.text
    except Exception as e:
      if attempt == max_retries - 1:
        raise
      wait_time = backoff_factor**attempt
      print(
        f"Attempt {attempt + 1} failed. Retrying in {wait_time} seconds...", e
      )
      time.sleep(wait_time)


def process_files():
  input_dir = "../gen/extracted_text"
  output_dir = "../gen/refined_text"

  # Create output directory if it doesn't exist
  os.makedirs(output_dir, exist_ok=True)

  for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
      input_path = os.path.join(input_dir, filename)
      output_path = os.path.join(output_dir, filename)

      print(f"Processing {filename}...")

      with open(input_path, encoding="utf-8") as infile:
        content = infile.read()

      try:
        refined_content = generate_refined_text(content)
        assert refined_content is not None

        with open(output_path, "w", encoding="utf-8") as outfile:
          outfile.write(refined_content)

        print(f"Refined content written to {output_path}")

      except Exception as e:
        print(f"Error processing {filename}: {e!s}")


if __name__ == "__main__":
  process_files()
