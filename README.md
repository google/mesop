# Mesop: Build delightful web apps quickly in Python 🚀

### Used at Google for rapid internal app development

Mesop is a Python-based UI framework that allows you to rapidly build web apps like demos and internal apps:

**Intuitive for UI novices ✨**

- Write UI in idiomatic Python code
- Easy to understand reactive UI paradigm
- Ready to use components

**Frictionless developer workflows 🏎️**

- Hot reload so the browser automatically reloads and preserves state
- Edit your UI code directly in the browser using the visual editor

**Flexible for delightful demos 🤩**

- Build custom UIs _without_ writing Javascript/CSS/HTML
- Compose your UI into components, which are just Python functions

**Edit your UI directly in the browser using the Visual Editor 🪄**

[![Visual Editor](https://img.youtube.com/vi/tvbO-Lqq_TA/0.jpg)](https://www.youtube.com/watch?v=tvbO-Lqq_TA)

## Write your first Mesop app in less than 10 lines of code...

[Demo app](https://mesop-y677hytkra-uc.a.run.app/text_io)

```python
import time

import mesop as me
import mesop.labs as mel


@me.page(path="/text_io", title="Text I/O Example")
def app():
  mel.text_io(
    upper_case_stream,
    title="Text I/O Example",
  )


def upper_case_stream(s: str):
  yield s.capitalize()
  time.sleep(0.5)
  yield s.capitalize() + "foo"
```

</div>

## Try it

**Step 1:** Install it

```sh
$ pip install mesop
```

**Step 2:** Copy the example above into `main.py`

**Step 3:** Run the app

```sh
$ mesop main.py
```

Learn more in [Getting Started](./getting_started.md).

## Disclaimer

_This is not an officially supported Google product._
