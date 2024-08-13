---
date: 2024-08-12
---

# Building a Docs Chatbot for Mesop with Mesop

## Why we built a Docs Chatbot

A big aspect of making Mesop accessible is answering questions both from the open-source community and internal company (Google) community. We noticed that a lot of similar (but not exactly the same) questions were coming up repeatedly, even ones covered by our docs. Since the early days of the project, we have invested significantly in our docs, trying to keep it up-to-date and relevant with examples. We use [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/), which has been a fantastic docs platform for our project, and have been using its search functionality.

Although Material for Mkdocs built-in search functionality is snappy (and operates entirely client-side), it can be finicky to use and requires users to search for the exact terms, otherwise it won't return any results. I suspected this was the main reason why users were asking us on our (corporate) chatroom or on GitHub issues/discussions - the docs were too hard to navigate!

Different startups in the space like [Inkeep](https://inkeep.com/) and [Mendable](https://www.mendable.ai/) have services to essentially provide a chatbot over your docs. Because Mesop is _not_ an official Google project, we have a shoestring budget so I looked at building a solution that would be inexpensive to maintain as Mesop's user base grows.

Before we dive into the technical details, let's take a look at the chatbot:

![Mesop Doc Chatbot](https://github.com/user-attachments/assets/728046b1-501a-4b1e-a757-aa0df0fbc72d)

You can interact with the chatbot by going to [Mesop docs site](https://google.github.io/mesop/) and clicking on the search button (or using the hotkey ⌘+K). It's simple chat interface that gives users a brief response and specific doc pages to look at.

## Overall architecture of the Docs Chatbot

The docs chatbot is essentially comprised of two parts:

1. A RAG-based LLM system that uses Mesop docs as the corpus
2. A chatbot-like UI that users can open on Mesop's doc site

For the first part, I used Llama Index which is a popular RAG framework that's very easy to get started with.  And for the second part, of course, I had to use Mesop and dogfood on our own UI framework!

## Basic RAG system

The first version of the RAG system was basically a slightly modified version of Llama index's [starter example](https://docs.llamaindex.ai/en/stable/getting_started/starter_example/):

```py
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
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    return index

index = build_or_load_index()
llm = Gemini(model="models/gemini-1.5-flash-latest")
query_engine = CitationQueryEngine.from_args(
  index,
  llm=llm,
  similarity_top_k=5,
  embedding_model=embed_model,
  streaming=True,
)
```

Much of this is pretty standard - the main difference is that I've used [CitationQueryEngine](https://docs.llamaindex.ai/en/stable/examples/query_engine/citation_query_engine/) so that the docs are explicitly cited. I wanted to do this to minimize the problem of hallucination and make this chatbot tool an educational tool to help users discover the right docs.

## Building the chat UI

I wanted to create a minimalist chat UI that would prominently display the sources.

I started off by forking the [chat component code](https://github.com/google/mesop/blob/main/mesop/labs/chat.py), which is something we encourage people to do when they build custom chat applications! It provides a good base with a straightforward UI and core chat functionality.

From there I made some modifications to make the UI look good as an embedded app. I also wanted to provide a few examples to make teach users how to use the chat app and I created prominent sources box so that users could open up the cited sources in a new page.

On of the tricky parts with building an embedded Mesop app is that the main docs site (built with Mkdocs Material) needs to interact with the Mesop chatbot app using cross-frame communications. With Mesop [web components](https://google.github.io/mesop/web-components/) you can write custom JavaScript to do this.

You can take a look at the final code [here](https://github.com/google/mesop/blob/17b9c18bfa03b997c0040939f6e4aff49d1f0bae/ai/docbot/main.py).

## Tuning the RAG system (aka Prompt Engineering)

After I built the end-to-end prototype, I started trying a few different prompts and I noticed the results were hit or miss. Oftentimes, it would decline to provide an answer, even though there were docs on the topic, or it cited pages that were not as relevant.

I knew I needed to start to adjusting the knobs with Llama Index (which there are many!). The hard part about this is that it's not one-size-fits-all, so Llama Index provides a lot of configurable options and it's up to you to figure out the right settings for your use case.

Because it's a highly iterative process, I wanted a faster way of comparing results before-and-after (e.g. different prompt, different retrieval settings, etc.). I created a simple [Python script](https://github.com/google/mesop/blob/main/ai/docbot/recorder.py) that basically had a set of prompts (e.g. commonly asked questions about Mesop) and ran them against the Llama Index query engine and recorded both the input (what the LLM saw) and the output (what the LLM produced / what the user will see).

Then, I created a barebones side-by-side eval viewer which is basically a five-column grid:

1. Prompt
2. LLM input (side A)
3. LLM output (side A)
4. LLM input (side B)
5. LLM output (side B)

![SxS Eval Viewer](https://github.com/user-attachments/assets/fe0f0d8f-7a1d-4e20-b5de-3841cf00cf6b)

This is kind of like the opposite of the end-user chatbot UI. It's ugly but it's very information-dense. Being able to see the LLM input and output together makes it easier to diagnose why you got a bad response. For example, from the input, you can see if any of the retrieved sources had relevant information, which could be a sign that you need to retrieve more documents (e.g. `similarity_top_k`).

Being able to see the two sides (e.g. I changed a setting like retrieving more documents, updating `similarity_top_k` to a larger number), I can quickly identify whether a change resulted in an improvement.

Creating these scrappy "single-user" UIs are invaluable - without this eval UI, I was tediously spot-checking a few prompts, which is both inefficient and insuffocient coverage. With the eval UI, I was able to rapidly check the results for a couple dozen prompts in about a minute or two.

Once I created this eval UI, I did probably a dozen or so iterations to try out different ideas:

- Custom prompts - I did a good chunk of prompt engineering (LINK)
- Hybrid search - LINK
- Number of documents retrieved - LINK

## Keeping it cheap

Thanks to the [recent Gemini Flash price reductions](https://developers.googleblog.com/en/gemini-15-flash-updates-google-ai-studio-gemini-api/#:~:text=Gemini%201.5%20Flash%20price%20decrease&text=To%20make%20this%20model%20even,tier%20as%20well%20as%20caching), running this chatbot is actually quite inexpensive.

- Embedding costs (~10 token per prompt) - free for [1500 requests per minute](https://ai.google.dev/pricing)
- LLM call (~1k token input, <100 token output)
    - Input: <1k tokens ($0.075 per 1M)
    - Output: <100 tokens ($0.30 per 1M)

For a thousand requests, it's $0.075 for input token costs and $0.03 cents for output token costs. That's around 10 cents total.

This means that 1M requests would cost $100. Not too bad!

To deploy the chatbot app and RAG system, I used huggingface spaces which is free.

## Conclusion

Mesop is an excellent tool for building AI apps, both user-facing ones and internal UIs.
