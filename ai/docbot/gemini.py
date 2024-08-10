import os

from llama_index.llms.gemini import Gemini

os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_FREE_API_KEY"]

resp = Gemini(model="models/gemini-1.5-flash-latest").complete(
  "Write a poem about a magic backpack"
)
print(resp)
