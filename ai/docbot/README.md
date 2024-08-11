---
title: Mesop Doc Bot
emoji: 👓
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
license: apache-2.0
app_port: 8080
---

# Docbot

Answers questions grounded based on docs

## Setup

From workspace root:

```sh
rm -rf ai/docbot/venv && \
virtualenv --python python3 ai/docbot/venv && \
source ai/docbot/venv/bin/activate && \
pip install -r ai/docbot/requirements.txt
```

## How to use

**Run app**:

```sh
mesop chat.py
```

**Create index**:

```sh
python docs_index.py --build-index
```

**Load (or create, if it doesn't exist yet) index**:

```sh
python docs_index.py
```

## Evals

- How do I test mesop app?
- What kind of components are there?
- How do I reset a text input?
- style a component
- Create a multi-page app
- Can I create custom components in Mesop?
- how do I do auth?
- call an API
- deploy mesop
- make mesop faster
- datepicker
- use JS library
- do real-time updates
- stream UI updates from LLM API
- debug mesop app
- is it production-ready?
- do form validation
- mobile
- async
- dark mode
- keyboard shortcuts
- drag and drop
- do infinite scroll
- make a row
- add tooltip
- render pandas dataframe
- add charts
- create a table
- handle file uploads
- use CLI flags
- create a link
- create a download link

## Roadmap

### UX

- Scroll to specific part of text? DONE
- Show code (syntax highlighting)
- Don't show sources which are not cited? done
- Renumber?? done
- File GitHub issue if the response isn't good DONE

### APIs

- Use Google embedding API? done

### Indexing

- Index GitHub issues / discussions?
  - https://docs.llamaindex.ai/en/stable/examples/usecases/github_issue_analysis/
- DONE filter out blog posts? (the --- mark settings)
- DONE filter out internal docs, e.g. bazel commands
- DONE set title for all pages OR retrieve title by using mkdocs.yml??
- Maybe load in the code snippets? Depends on whether that's a goal.

### Docs TODOs:

- Why doesn't mesop have this new feature? attribute is missing
