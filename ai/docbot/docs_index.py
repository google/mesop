import logging
import os
import sys

from llama_index.core import (
  PromptTemplate,
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

CITATION_QA_TEMPLATE = PromptTemplate(
  "Please provide an answer based solely on the provided sources. "
  "When referencing information from a source, "
  "cite the appropriate source(s) using their corresponding numbers. "
  "Every answer should include at least one source citation. "
  "Only cite a source when you are explicitly referencing it. "
  "If you are sure NONE of the sources are helpful, then say: 'Sorry, I didn't find any docs about this.'"
  "If you are not sure if any of the sources are helpful, then say: 'You might find this helpful', where 'this' is the source's title.'"
  "DO NOT say Source 1, Source 2, etc. Only reference sources like this: [1], [2], etc."
  "I want you to pick just ONE source to answer the question."
  "For example:\n"
  "Source 1:\n"
  "The sky is red in the evening and blue in the morning.\n"
  "Source 2:\n"
  "Water is wet when the sky is red.\n"
  "Query: When is water wet?\n"
  "Answer: Water will be wet when the sky is red [2], "
  "which occurs in the evening [1].\n"
  "Now it's your turn. Below are several numbered sources of information:"
  "\n------\n"
  "{context_str}"
  "\n------\n"
  "Query: {query_str}\n"
  "Answer: "
)

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
    for doc in documents:
      doc.excluded_llm_metadata_keys = ["url"]
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
    citation_qa_template=CITATION_QA_TEMPLATE,
    similarity_top_k=5,
    embedding_model=embed_model,
    streaming=True,
  )

  blocking_query_engine = CitationQueryEngine.from_args(
    index,
    llm=llm,
    citation_qa_template=CITATION_QA_TEMPLATE,
    similarity_top_k=5,
    embedding_model=embed_model,
    streaming=False,
  )
  # TODO: replace with proper mechanism for persisting objects
  # across hot reloads
  me._query_engine = query_engine


NEWLINE = "\n"

cache = {}


def ask(query: str):
  return query_engine.query(query)
