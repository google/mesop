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

**Record eval results**

```py
$ python recorder.py --out-dir gen/evals/one_source
```

**View eval results**

```py
$ EVAL_DIR=gen/evals/no_source_1 EVAL_DIR_2=gen/evals/one_source mesop eval_viewer.py
```

## Roadmap

TODOs:

- Respect dark themes into frame
- Auto-focus into prompt (via post message) _DONE_
- Support ESC to close iframe _DONE_
- Do evals against suggested questions _DONE_
- Prompt engineer
  - Do not show code _skip_
  - File new issue if asking for feature that doesn't exist _skip_

MAYBE:

- Ask Mesop to consolidate sources from the same page

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
