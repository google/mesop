# Overview

Optic is a Python-based UI framework that allows you to rapidly build web demos. Engineers without frontend experience can build web UIs by writing idiomatic Python code.

> Disclaimer: *This is not an officially supported Google product.*

## Example app

```python
import optic as op

@op.on(op.ClickEvent)
def chat(state: State, action: op.ClickEvent):
    response = streaming_api_call(...)
    for chunk in response:
        state.text += chunk.text
        yield state

def main():
    op.button("Start chat", on_click=chat)
```

## Getting Started

> TODO: Optic is still under development
