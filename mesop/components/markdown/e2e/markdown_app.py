import mesop as me

SAMPLE_MARKDOWN = """
# Sample Markdown Document

Regular code block:

```
hello
```

Python code block:

Syntax 1:

```python
def foo():
  print("Hello, World 1!")

foo()
```

Syntax 2:

``` python
def foo():
  print("Hello, World 2!")

foo()
```

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

## Inline Code
Inline `code`

## Table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
"""


UPDATED_MARKDOWN = """
Testing code blocks get rerendered.

Python code block:

Syntax 1:

```python
def foo():
  print("Hello, World 3!")

foo()
```

Syntax 2:

``` python
def foo():
  print("Hello, World 4!")

foo()
```

"""


@me.stateclass
class State:
  markdown: str = SAMPLE_MARKDOWN


@me.page(path="/components/markdown/e2e/markdown_app")
def app():
  state = me.state(State)
  me.button(label="Updated markdown", on_click=on_click)
  me.markdown(
    text=state.markdown,
    style=me.Style(
      margin=me.Margin.all(4),
      border=me.Border.all(
        me.BorderSide(width=2, color="pink", style="solid"),
      ),
    ),
  )


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.markdown = UPDATED_MARKDOWN
