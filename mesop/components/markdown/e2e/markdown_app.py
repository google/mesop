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
  print("Hello, World!")

foo()
```

Syntax 2:

``` python
def foo():
  print("Hello, World!")

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

## Code
Inline `code`
"""


@me.stateclass
class State:
  select_item: str


def on_select(e):
  me.state(State).select_item = e.value


@me.page(path="/components/markdown/e2e/markdown_app")
def app():
  state = me.state(State)
  if state.select_item:
    me.text("Select: " + state.select_item)
  me.markdown(
    """Creative writing is a powerful tool for exploring the human experience. It allows writers to <a class="explore imagination, create worlds">weave intricate tales</a> and delve into the depths of human emotion. Whether it's crafting captivating narratives, writing evocative poetry, or composing thought-provoking essays, creative writing offers a unique opportunity for self-expression. <a class="describe types of creative writing, what makes it different from other forms of writing">The creative process</a> involves tapping into one's imagination,  experiencing the world through different lenses, and finding unique ways to communicate ideas. It is a journey of discovery, where writers are constantly challenged to push their boundaries and find new ways to engage their audience.

One of the most rewarding aspects of creative writing is its ability to connect with readers on an emotional level.  <a class="what are the emotions that creative writing can evoke">Through carefully crafted words and evocative imagery</a>, writers can transport readers to different worlds, introduce them to unforgettable characters, and evoke a range of emotions. This ability to create empathy and understanding is what makes creative writing so powerful and enduring. <a class="why is creative writing important to society">As a form of artistic expression</a>, creative writing transcends cultural boundaries and allows us to connect with each other on a deeper level. It can provide solace, inspiration, and a sense of belonging in a world that can often feel isolating.
""",
    on_select=on_select,
  )

  me.markdown(
    text=SAMPLE_MARKDOWN,
    style=me.Style(
      margin=me.Margin.all(4),
      border=me.Border.all(
        me.BorderSide(width=2, color="pink", style="solid"),
      ),
    ),
  )
