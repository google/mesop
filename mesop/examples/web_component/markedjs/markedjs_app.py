import mesop as me
from mesop.examples.web_component.markedjs.markedjs_component import (
  markedjs_component,
)

SAMPLE_MARKDOWN = """
# Sample Markdown Document

## Table of Contents
1. [Headers](#headers)
2. [Emphasis](#emphasis)
3. [Lists](#lists)
4. [Links](#links)
5. [Code](#code)
6. [Blockquotes](#blockquotes)
7. [Tables](#tables)
8. [Horizontal Rules](#horizontal-rules)

## Headers
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6

## Emphasis
*Italic text* or _Italic text_
**Bold text** or __Bold text__
***Bold and Italic*** or ___Bold and Italic___

## Lists

### Unordered List
- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2

### Ordered List
1. First item
2. Second item
   1. Subitem 2.1
   2. Subitem 2.2

## Links
[Google](https://www.google.com/)

## Code Inline

This is `var code = 'code';`


## Code

```python
import mesop as me


@me.page(path="/hello_world")
def app():
  me.text("Hello World")
```

```mermaid
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?
```

## Table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell | Content Cell
"""


@me.stateclass
class State:
  markdown: str = SAMPLE_MARKDOWN


@me.page(
  path="/web_component/markedjs/markedjs_app",
  stylesheets=[
    # Other themes here: https://www.jsdelivr.com/package/npm/highlight.js?tab=files&path=styles
    "https://cdn.jsdelivr.net/npm/highlight.js@11.10.0/styles/night-owl.min.css",
  ],
  security_policy=me.SecurityPolicy(
    allowed_connect_srcs=["https://cdn.jsdelivr.net"],
    allowed_script_srcs=["https://cdn.jsdelivr.net"],
    # CAUTION: this disables an important web security feature and
    # should not be used for most mesop apps.
    #
    # Disabling trusted types because we need DomPurifier is not listed in TrustedHTML
    # assignment.
    dangerously_disable_trusted_types=True,
  ),
)
def page():
  state = me.state(State)
  with me.box(
    style=me.Style(display="flex", gap=20, padding=me.Padding.all(20))
  ):
    with me.box(style=me.Style(flex_grow=1)):
      me.textarea(
        value=state.markdown,
        on_blur=on_blur,
        style=me.Style(width="100%", height="100%"),
        autosize=True,
      )
    with me.box(
      style=me.Style(
        padding=me.Padding.all(10),
        border=me.Border.all(me.BorderSide(width=1, style="solid")),
      )
    ):
      markedjs_component(state.markdown)


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.markdown = e.value
