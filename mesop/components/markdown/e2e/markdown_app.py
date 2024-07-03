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

## Table

First Header  | Second Header
------------- | -------------
Content Cell { .foo }  | Content Cell { .foo }
Content Cell { .bar } | Content Cell { .bar }
"""


@me.page(path="/components/markdown/e2e/markdown_app")
def app():
  me.markdown(
    text=SAMPLE_MARKDOWN,
    style=me.Style(
      margin=me.Margin.all(4),
      border=me.Border.all(
        me.BorderSide(width=2, color="pink", style="solid"),
      ),
    ),
  )
