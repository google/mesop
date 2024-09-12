import mesop as me

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

## Inline Code

Inline `code`

## Code

```python
import mesop as me


@me.page(path="/hello_world")
def app():
  me.text("Hello World")
```


## Table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
"""


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/markdown_demo",
  on_load=on_load,
)
def app():
  with me.box(
    style=me.Style(background=me.theme_var("surface-container-lowest"))
  ):
    me.markdown(SAMPLE_MARKDOWN, style=me.Style(margin=me.Margin.all(15)))
