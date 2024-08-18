import datetime
import os

import google.generativeai as genai
from google.generativeai import caching

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

8. Only output the python code.

Here is is the code for the app:

```
<APP_CODE>
```

Here is a description of the changes I want:

<APP_CHANGES>

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


def adjust_mesop_app(code: str, msg: str) -> str:
  model = make_model()
  response = model.generate_content(
    REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
      "<APP_CHANGES>", msg
    ),
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
  )
  return response.text.strip().removeprefix("```python").removesuffix("```")
