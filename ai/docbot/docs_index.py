# !pip install -q llama-index google-generativeai
# !pip install llama-index-llms-gemini
# !pip install llama-index-embeddings-google
import os

from llama_index.core import Settings
from llama_index.embeddings.google import GeminiEmbedding
from llama_index.llms.gemini import Gemini

os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_FREE_API_KEY"]


# from llama_index.embeddings.gemi import OpenAIEmbedding

import logging
import os
import sys

from llama_index.core import (
  SimpleDirectoryReader,
  StorageContext,
  VectorStoreIndex,
  load_index_from_storage,
)
from llama_index.core.query_engine import CitationQueryEngine

import mesop as me

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_meta(file_path: str) -> dict[str, str]:
  with open(file_path) as f:
    title = f.readline().strip()
    if title.startswith("# "):
      title = title[2:]
  # truncate everything up to and including ../../docs/ with ""
  file_path = file_path.replace(".md", "")
  CONST = "../../docs/"
  docs_index = file_path.index(CONST)
  docs_path = file_path[docs_index + len(CONST) :]
  # title = read the first line of the file

  url = "https://google.github.io/mesop/" + docs_path

  print(f"URL: {url}")
  return {
    "url": url,
    "title": title,
  }


# embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

embed_model = GeminiEmbedding(
  model_name="models/text-embedding-004", api_key=os.environ["GOOGLE_API_KEY"]
)
Settings.embed_model = embed_model

# check if storage already exists
PERSIST_DIR = "./gen"


def build_or_load_index():
  if not os.path.exists(PERSIST_DIR) or "--build-index" in sys.argv:
    print("Building index")
    # load the documents and create the index
    documents = SimpleDirectoryReader(
      "../../docs/",
      required_exts=[
        ".md",
      ],
      exclude=["**/docs/showcase.md", "**/docs/demo.md"],
      file_metadata=get_meta,
      recursive=True,
    ).load_data()
    # Create the index with the specified embedding model
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index
  else:
    print("Loading index")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    return index


if me.runtime().is_hot_reload_in_progress:
  print("Hot reload - skip building index!")
else:
  index = build_or_load_index()
  llm = Gemini(model="models/gemini-1.5-flash-latest")
  query_engine = CitationQueryEngine.from_args(
    index,
    llm=llm,
    similarity_top_k=5,
    embedding_model=embed_model,
    streaming=True,
    # similarity_top_k=3,
    # # here we can control how granular citation sources are, the default is 512
    # citation_chunk_size=512,
  )

# query_engine = index.as_query_engine(
#   llm=llm,
#   similarity_top_k=5,
#   embedding_model=embed_model,
#   streaming=True,
# )
# response = query_engine.query("What is Mesop?")
# print("---")
# print(response.response)
# print("\nSources:")
# for source_node in response.source_nodes:
#   print(f"- {source_node.node.metadata.get('url', 'Unknown URL')}")
#   print(f"  Relevance: {source_node.score:.2f}")
#   print(f"  Content: {source_node.node.get_content()}")  # Print first 100 chars
#   print()

NEWLINE = "\n"


def ask(query: str):
  response_stream = query_engine.query(query)
  return response_stream
