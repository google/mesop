import datetime
import os
import re
from os import getenv

import google.generativeai as genai
from google.generativeai import caching
from openai import OpenAI

from mesop.utils.runfiles import get_runfile_location

with open(get_runfile_location("mesop/mesop/llm/prompt.txt")) as f:
  SYSTEM_INSTRUCTION = f.read()


REVISE_APP_BASE_PROMPT = """
Your task is to modify a Mesop app given the code and a description.

Make sure to remember these rules when making modifications:
1. For the @me.page decorator, keep it the same as the original *unless* you need to modify on_load.
2. Event handler functions cannot use lambdas. You must use functions.
3. Event handle functions only pass in the event type. They do not accept extra parameters.
4. For padding, make sure to use the the `me.Padding` object rather than a string or int.
5. For margin, make sure to use the the `me.Margin` object rather than a string or int.
6. For border, make sure to use the the `me.Border` and `me.BorderSide` objects rather than a string.
7. For buttons, prefer using type="flat", especially if it is the primary button.
- Make the apps beautiful and visually pleasing:
1. Use rounded corners (border_radius) for components to create a modern look
2. Apply consistent spacing using Padding and Margin
3. Utilize theme variables (me.theme_var) for colors to ensure a cohesive design
4. Implement a clear visual hierarchy with appropriate typography styles
5. Use the Box component to create structured layouts
6. Include subtle animations or transitions for improved user experience
7. Ensure the design is responsive and adapts well to different screen sizes
8. Incorporate appropriate icons to enhance visual communication
9. Use contrasting colors for important elements to draw attention
10. Implement proper alignment and grouping of related elements
Remember to follow Mesop best practices and use only the components and styles explicitly mentioned in the documentation.

I want the output to be Python code using the following diff format with separate chunks for original and updated code.
Existing app code:
```
[APP_CODE]
```

User instructions:
[USER_INSTRUCTIONS]

Diff output:
<<<<<<< ORIGINAL
[ORIGINAL_CODE]
=======
[UPDATED_CODE]
>>>>>>> UPDATED

Here's an example:

Existing app code:
```
import mesop as me
import mesop.labs as mel

@me.stateclass
class State:
    count: int = 0

def increment(e: me.ClickEvent):
    state = me.state(State)
    state.count += 1

@me.page()
def counter_page():
    state = me.state(State)
    me.text(f"Count: {state.count}")
    me.button("Increment", on_click=increment, type="flat")
```

User instructions:
Add a decrement button


Diff output:
<<<<<<< ORIGINAL
@me.page()
def counter_page():
    state = me.state(State)
    me.text(f"Count: {state.count}")
    me.button("Increment", on_click=increment, type="flat")
=======
def decrement(e: me.ClickEvent):
    state = me.state(State)
    state.count -= 1

@me.page()
def counter_page():
    state = me.state(State)
    me.text(f"Count: {state.count}")
    me.button("Increment", on_click=increment, type="flat")
    me.button("Decrement", on_click=decrement, type="flat")
>>>>>>> UPDATED

OK, now that I've shown you an example, let's do this for real.

Existing app code:
```
<APP_CODE>
```

User instructions:
<APP_CHANGES>

Diff output:
""".strip()

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 32768,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]


def make_model() -> genai.GenerativeModel:
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  # cache = get_or_create_cache()
  # model = genai.GenerativeModel.from_cached_content(cached_content=cache)
  # return model
  return genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-001",
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=safety_settings,
    generation_config=generation_config,
  )


def get_or_create_cache() -> caching.CachedContent:
  # prompt: get or create a cache
  cache_list = list(caching.CachedContent.list())
  if cache_list:
    cache_list[0]
    assert cache_list[0].display_name == "mesop_context"

    cache = cache_list[0]
    print("reuse existing cache", cache)
  else:
    cache = create_cache()
    print("create new cache", cache)
  return cache


def create_cache() -> caching.CachedContent:
  # Create a cache with a 5 minute TTL
  return caching.CachedContent.create(
    model="models/gemini-1.5-flash-001",
    display_name="mesop_context",  # used to identify the cache
    system_instruction=SYSTEM_INSTRUCTION,
    ttl=datetime.timedelta(minutes=10),
  )


def apply_patch(original_code: str, llm_output: str) -> str:
  # Extract the diff content
  diff_pattern = r"<<<<<<< ORIGINAL(.*?)=======\n(.*?)>>>>>>> UPDATED"
  matches = re.findall(diff_pattern, llm_output, re.DOTALL)
  patched_code = original_code
  if len(matches) == 0:
    print("[WARN] No diff found:", llm_output)
  for original, updated in matches:
    original = original.strip()
    updated = updated.strip()

    # Replace the original part with the updated part
    patched_code = patched_code.replace(original, updated)

  return patched_code


def adjust_mesop_app(code: str, msg: str) -> str:
  return adjust_mesop_app_openrouter(code, msg)


def adjust_mesop_app_gemini(code: str, msg: str) -> str:
  model = make_model()
  response = model.generate_content(
    REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
      "<APP_CHANGES>", msg
    ),
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
  )

  llm_output = response.text.strip()
  print("[INFO] LLM output:", llm_output)
  patched_code = apply_patch(code, llm_output)

  return patched_code


# open router client
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPEN_ROUTER_API_KEY"),
)

# Fireworks client
# client = OpenAI(
#     base_url = "https://api.fireworks.ai/inference/v1",
#     api_key=getenv("FIREWORKS_API_KEY"),
# )

# Groq client
# client = OpenAI(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=getenv("GROQ_API_KEY")
# )

# ollama client
# client = OpenAI(
#     base_url = 'http://localhost:11434/v1',
#     api_key='ollama', # required, but unused
# )

# together client
# client = OpenAI(
#   api_key=os.environ.get("TOGETHER_API_KEY"),
#   base_url="https://api.together.xyz/v1",
# )


def adjust_mesop_app_openrouter(code: str, msg: str) -> str:
  completion = client.chat.completions.create(
    #  model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    #  model = "deepseek-coder-v2",
    #  model="llama-3.1-70b-versatile",
    model="deepseek/deepseek-coder",
    max_tokens=10_000,
    messages=[
      {
        "role": "system",
        "content": SYSTEM_INSTRUCTION,
      },
      {
        "role": "user",
        "content": REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
          "<APP_CHANGES>", msg
        ),
      },
    ],
  )
  print("[INFO] LLM output:", completion.choices[0].message.content)
  llm_output = completion.choices[0].message.content
  patched_code = apply_patch(code, llm_output)

  return patched_code
