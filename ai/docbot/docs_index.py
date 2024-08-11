import logging
import os
import sys

from llama_index.core import (
  Settings,
  SimpleDirectoryReader,
  StorageContext,
  VectorStoreIndex,
  load_index_from_storage,
)
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.google import GeminiEmbedding
from llama_index.llms.gemini import Gemini

import mesop as me

os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_meta(file_path: str) -> dict[str, str]:
  with open(file_path) as f:
    title = f.readline().strip()
    if title.startswith("# "):
      title = title[2:]
    else:
      title = (
        file_path.split("/")[-1]
        .replace(".md", "")
        .replace("-", " ")
        .capitalize()
      )
  # truncate everything up to and including ../../docs/ with ""
  file_path = file_path.replace(".md", "")
  CONST = "../../docs/"
  docs_index = file_path.index(CONST)
  docs_path = file_path[docs_index + len(CONST) :]

  url = "https://google.github.io/mesop/" + docs_path

  print(f"URL: {url}")
  return {
    "url": url,
    "title": title,
  }


embed_model = GeminiEmbedding(
  model_name="models/text-embedding-004", api_key=os.environ["GOOGLE_API_KEY"]
)
Settings.embed_model = embed_model

PERSIST_DIR = "./gen"


def build_or_load_index():
  if not os.path.exists(PERSIST_DIR) or "--build-index" in sys.argv:
    print("Building index")

    documents = SimpleDirectoryReader(
      "../../docs/",
      required_exts=[
        ".md",
      ],
      exclude=[
        "showcase.md",
        "demo.md",
        "blog",
        "internal",
      ],
      file_metadata=get_meta,
      recursive=True,
    ).load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index
  else:
    print("Loading index")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    return index


if me.runtime().is_hot_reload_in_progress:
  print("Hot reload - skip building index!")
  query_engine = me._query_engine

else:
  index = build_or_load_index()
  llm = Gemini(model="models/gemini-1.5-flash-latest")

  query_engine = CitationQueryEngine.from_args(
    index,
    llm=llm,
    similarity_top_k=5,
    embedding_model=embed_model,
    streaming=True,
  )
  # TODO: replace with proper mechanism for persisting objects
  # across hot reloads
  me._query_engine = query_engine


NEWLINE = "\n"


def ask(query: str):
  response_stream = query_engine.query(query)
  return response_stream
