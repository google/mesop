"""
Note: this test doesn't run on GitHub actions.

You must run this manually:
$ uv run src/ai/common/diff_test.py
"""

import difflib

import pytest

from ai.common.diff import apply_udiff


def test_apply_udiff_basic():
  original_code = """
def hello():
    print('Hello')
    print('End')
""".strip()

  udiff = """
@@ .. @@
 def hello():
-    print('Hello')
+    print('World')
     print('End')
""".strip()

  expected_result = """
def hello():
    print('World')
    print('End')
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_indentation():
  original_code = """
    def hello():
        print('before')
        print('Hello')
        print('End')
""".strip("\n")
  print(f"original_code\n{original_code}")
  udiff = """
@@ .. @@
     def hello():
         print('before')
-        print('Hello')
+        print('World')
         print('End')
""".strip()

  expected_result = """
    def hello():
        print('before')
        print('World')
        print('End')
""".strip("\n")

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_forgiving_of_indentation():
  original_code = """
    def hello():
        print('before')
        print('Hello')
        print('End')
""".strip("\n")
  print(f"original_code\n{original_code}")
  udiff = """
@@ .. @@
    def hello():
        print('before')
-        print('Hello')
+        print('World')
         print('End')
""".strip()

  expected_result = """
    def hello():
        print('before')
        print('World')
        print('End')
""".strip("\n")

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_no_context_after():
  original_code = """
def hello():
    print('Hello')
""".strip()

  udiff = """
@@ .. @@
 def hello():
-    print('Hello')
+    print('World')
""".strip()

  expected_result = """
def hello():
    print('World')
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_only_add():
  original_code = """
def hello():
    print('Hello')
""".strip()

  udiff = """
@@ .. @@
 def hello():
     print('Hello')
+    print('World')
""".strip()

  expected_result = """
def hello():
    print('Hello')
    print('World')
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_other_code():
  original_code = """
def foo():
    pass

def hello():
    print('Hello')
""".strip()

  udiff = """
@@ .. @@
 def hello():
     print('Hello')
+    print('World')
""".strip()

  expected_result = """
def foo():
    pass

def hello():
    print('Hello')
    print('World')
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_multiple_hunks():
  original_code = """
def greet(name):
    print('Hello')
    return 'Greeting complete'

def farewell(name):
    print('Goodbye')
    return 'Farewell complete'
""".strip()

  udiff = """
@@ .. @@
 def greet(name):
-    print('Hello')
+    print(f'Hello, {name}!')
     return 'Greeting complete'
@@ .. @@
 def farewell(name):
-    print('Goodbye')
+    print(f'Goodbye, {name}!')
     return 'Farewell complete'
""".strip()

  expected_result = """
def greet(name):
    print(f'Hello, {name}!')
    return 'Greeting complete'

def farewell(name):
    print(f'Goodbye, {name}!')
    return 'Farewell complete'
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_code_blocks():
  original_code = """
def hello():
    print('Hello')
    print('End')
""".strip()

  udiff = """
I'm thinking
```
@@ .. @@
 def hello():
-    print('Hello')
+    print('World')
     print('End')
```
Some text afterwards
""".strip()

  expected_result = """
def hello():
    print('World')
    print('End')
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_real():
  original_code = """
import mesop as me


@me.page(path="/simple")
def page():
  me.text("Hello, world!")
""".strip()

  udiff = """
```
@@ -1,6 +1,11 @@
 import mesop as me


 @me.page(path="/simple")
 def page():
-  me.text("Hello, world!")
+  me.text("Replaced")
```

This modification creates a side-by-side layout.
""".strip()

  expected_result = """
import mesop as me


@me.page(path="/simple")
def page():
  me.text("Replaced")
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_result)


def test_apply_udiff_real_2():
  original_code = """
import mesop as me


@me.page(path="/simple")
def page():
  me.text("Hello, world!")
""".strip()

  udiff = """
```
@@ ... @@
 import mesop as me

+@me.stateclass
+class PageState:
+    feedback: str = ""

+
+def submit_feedback(event: me.ClickEvent):
+    state = me.state(PageState)
+    print(f"Feedback: {state.feedback}")
+
+
 @me.page(path="/simple")
 def page():
-  me.text("Hello, world!")
+  state = me.state(PageState)
+  me.text("Hello, world!")
+  me.input(label="Your feedback", value=state.feedback, on_input=lambda e: state.feedback := e.value)
+  me.button("Submit", on_click=submit_feedback, type="flat")
```
""".strip()

  assert apply_udiff(original_code, udiff).has_error is False


def test_apply_udiff_real_3():
  original_code = """
import mesop as me


@me.stateclass
class State:
  count: int


def increment(e: me.ClickEvent):
  state = me.state(State)
  state.count += 1


@me.page()
def page():
  state = me.state(State)

  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=16,
      padding=me.Padding.all(16),
    )
  ):
    me.text(f"Count: {state.count}", type="headline-4")
    me.button("Increment", on_click=increment, type="flat")
""".strip()

  udiff = """
```
@@ ... @@
 def increment(e: me.ClickEvent):
   state = me.state(State)
   state.count += 1


+def decrement(e: me.ClickEvent):
+  state = me.state(State)
+  state.count -= 1
+
+
 @me.page()
 def page():
   state = me.state(State)

   with me.box(
     style=me.Style(
       display="flex",
       flex_direction="column",
       gap=16,
       padding=me.Padding.all(16),
     )
   ):
     me.text(f"Count: {state.count}", type="headline-4")
     me.button("Increment", on_click=increment, type="flat")
+    me.button("Decrement", on_click=decrement, type="flat")
```
""".strip()

  expected_code = """
import mesop as me


@me.stateclass
class State:
  count: int


def increment(e: me.ClickEvent):
  state = me.state(State)
  state.count += 1


def decrement(e: me.ClickEvent):
  state = me.state(State)
  state.count -= 1


@me.page()
def page():
  state = me.state(State)

  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=16,
      padding=me.Padding.all(16),
    )
  ):
    me.text(f"Count: {state.count}", type="headline-4")
    me.button("Increment", on_click=increment, type="flat")
    me.button("Decrement", on_click=decrement, type="flat")
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_code)


def test_apply_udiff_real_4():
  original_code = """
import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  me.text(text="headline-1: Hello, world!", type="headline-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-2: Hello, world!", type="headline-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="Welcome to Mesop!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-4: Hello, world!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-5: Hello, world!", type="headline-5", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-6: Hello, world!", type="headline-6", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-1: Hello, world!", type="subtitle-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-2: Hello, world!", type="subtitle-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="body-1: Hello, world!", type="body-1", style=me.Style(color=me.theme_var("on-surface"), font_size=18))
  me.text(text="body-2: Hello, world!", type="body-2", style=me.Style(color=me.theme_var("on-surface")))
  me.text(text="caption: Hello, world!", type="caption", style=me.Style(color=me.theme_var("on-surface-variant")))
  me.text(text="button: Hello, world!", type="button", style=me.Style(color=me.theme_var("primary")))
  wrap_button()

  with me.box(style=me.Style(padding=me.Padding.all(24), background=me.theme_var("surface"))):
    me.text("inside box1", style=me.Style(color=me.theme_var("on-surface")))
    me.text("inside box2", style=me.Style(color=me.theme_var("on-surface")))


@me.component
def wrap_button():
  me.button("button")
""".strip()

  udiff = """
@@ .. @@

   me.text(text="headline-6: Hello, world!", type="headline-6", style=me.Style(color=me.theme_var("primary")))
   me.text(text="subtitle-1: Hello, world!", type="subtitle-1", style=me.Style(color=me.theme_var("primary")))
   me.text(text="subtitle-2: Hello, world!", type="subtitle-2", style=me.Style(color=me.theme_var("primary")))
-  me.text(text="body-1: Hello, world!", type="body-1", style=me.Style(color=me.theme_var("on-surface"), font_size=18))
+  me.text(text="This is body-1 text.", type="body-1", style=me.Style(color=me.theme_var("on-surface"), font_size=18))
   me.text(text="body-2: Hello, world!", type="body-2", style=me.Style(color=me.theme_var("on-surface")))
   me.text(text="caption: Hello, world!", type="caption", style=me.Style(color=me.theme_var("on-surface-variant")))
   me.text(text="button: Hello, world!", type="button", style=me.Style(color=me.theme_var("primary")))
""".strip()

  expected_code = """
import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  me.text(text="headline-1: Hello, world!", type="headline-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-2: Hello, world!", type="headline-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="Welcome to Mesop!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-4: Hello, world!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-5: Hello, world!", type="headline-5", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-6: Hello, world!", type="headline-6", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-1: Hello, world!", type="subtitle-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-2: Hello, world!", type="subtitle-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="This is body-1 text.", type="body-1", style=me.Style(color=me.theme_var("on-surface"), font_size=18))
  me.text(text="body-2: Hello, world!", type="body-2", style=me.Style(color=me.theme_var("on-surface")))
  me.text(text="caption: Hello, world!", type="caption", style=me.Style(color=me.theme_var("on-surface-variant")))
  me.text(text="button: Hello, world!", type="button", style=me.Style(color=me.theme_var("primary")))
  wrap_button()

  with me.box(style=me.Style(padding=me.Padding.all(24), background=me.theme_var("surface"))):
    me.text("inside box1", style=me.Style(color=me.theme_var("on-surface")))
    me.text("inside box2", style=me.Style(color=me.theme_var("on-surface")))


@me.component
def wrap_button():
  me.button("button")
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_code)


def test_apply_udiff_make_sure_negative_lines_are_used_for_context_matching():
  original_code = """
import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/box",
)
def app():
  with me.box(style=me.Style(background="red", padding=me.Padding.all(16))):
    with me.box(
      style=me.Style(
        background="green",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="pink", style="solid"),
          vertical=me.BorderSide(width=2, color="orange", style="solid"),
        ),
      )
    ):
      me.text(text="hi1")
      me.text(text="hi2")

    with me.box(
      style=me.Style(
        background="blue",
        height=50,
        margin=me.Margin.all(16),
        border=me.Border.all(
          me.BorderSide(width=2, color="yellow", style="dotted")
        ),
        border_radius=10,
      )
    ):
      me.text(text="Example with all sides bordered")

    with me.box(
      style=me.Style(
        background="purple",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          vertical=me.BorderSide(width=4, color="white", style="double")
        ),
      )
    ):
      me.text(text="Example with top and bottom borders")

    with me.box(
      style=me.Style(
        background="cyan",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="black", style="groove")
        ),
      )
    ):
      me.text(text="Example with left and right borders")
""".strip()

  udiff = """
@@ .. @@

     ):
       me.text(text="Example with top and bottom borders")

     with me.box(
       style=me.Style(
-        background="cyan",
-        height=50,
-        margin=me.Margin.symmetric(vertical=24, horizontal=12),
-        border=me.Border.symmetric(
-          horizontal=me.BorderSide(width=2, color="black", style="groove")
-        ),
+        display="flex",
+        align_items="center",
+        background=me.theme_var("surface"),
+        height=60,
+        margin=me.Margin.symmetric(vertical=16, horizontal=12),
+        border=me.Border.all(me.BorderSide(width=1, color=me.theme_var("outline"))),
+        border_radius=8,
+        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
       )
     ):
-      me.text(text="Example with left and right borders")
+      me.icon(icon="border_left", style=me.Style(margin=me.Margin(right=8), color=me.theme_var("primary")))
+      me.text(
+        text="Example with left and right borders",
+        style=me.Style(color=me.theme_var("on-surface"), font_size=16, font_weight=500)
+      )
""".strip()

  expected_code = """
import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/box",
)
def app():
  with me.box(style=me.Style(background="red", padding=me.Padding.all(16))):
    with me.box(
      style=me.Style(
        background="green",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="pink", style="solid"),
          vertical=me.BorderSide(width=2, color="orange", style="solid"),
        ),
      )
    ):
      me.text(text="hi1")
      me.text(text="hi2")

    with me.box(
      style=me.Style(
        background="blue",
        height=50,
        margin=me.Margin.all(16),
        border=me.Border.all(
          me.BorderSide(width=2, color="yellow", style="dotted")
        ),
        border_radius=10,
      )
    ):
      me.text(text="Example with all sides bordered")

    with me.box(
      style=me.Style(
        background="purple",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          vertical=me.BorderSide(width=4, color="white", style="double")
        ),
      )
    ):
      me.text(text="Example with top and bottom borders")

    with me.box(
      style=me.Style(
        display="flex",
        align_items="center",
        background=me.theme_var("surface"),
        height=60,
        margin=me.Margin.symmetric(vertical=16, horizontal=12),
        border=me.Border.all(me.BorderSide(width=1, color=me.theme_var("outline"))),
        border_radius=8,
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
      )
    ):
      me.icon(icon="border_left", style=me.Style(margin=me.Margin(right=8), color=me.theme_var("primary")))
      me.text(
        text="Example with left and right borders",
        style=me.Style(color=me.theme_var("on-surface"), font_size=16, font_weight=500)
      )
""".strip()

  result = apply_udiff(original_code, udiff)
  assert_code(result.result, expected_code)


def assert_code(actual_code: str, expected_code: str):
  if actual_code != expected_code:
    print("Expected:")
    print(expected_code)
    print("Got:")
    print(actual_code)

    print("*** DIFF ***")
    diff = difflib.unified_diff(
      expected_code.splitlines(keepends=True),
      actual_code.splitlines(keepends=True),
      fromfile="Expected",
      tofile="Got",
      n=3,
    )
    print("".join(diff))
  assert actual_code == expected_code


if __name__ == "__main__":
  pytest.main()
