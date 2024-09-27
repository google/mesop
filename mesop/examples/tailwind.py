import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  stylesheets=[
    "/assets/tailwind.css",
  ],
  path="/tailwind",
)
def app():
  with me.box(classes="grid grid-cols-10 gap-2"):
    with me.box(classes="bg-sky-50 aspect-square"):
      pass
    with me.box(classes="bg-sky-100 aspect-square"):
      pass
    with me.box(classes="bg-sky-200 aspect-square"):
      pass
    with me.box(classes="bg-sky-300 aspect-square"):
      pass
    with me.box(classes="bg-sky-400 aspect-square"):
      pass
    with me.box(classes="bg-sky-500 aspect-square"):
      pass
    with me.box(classes="bg-sky-600 aspect-square"):
      pass
    with me.box(classes="bg-sky-700 aspect-square"):
      pass
    with me.box(classes="bg-sky-800 aspect-square"):
      pass
    with me.box(classes="bg-sky-900 aspect-square"):
      pass

  with me.box(classes="grid grid-cols-10 gap-2"):
    with me.box(classes="bg-blue-50 aspect-square"):
      pass
    with me.box(classes="bg-blue-100 aspect-square"):
      pass
    with me.box(classes="bg-blue-200 aspect-square"):
      pass
    with me.box(classes="bg-blue-300 aspect-square"):
      pass
    with me.box(classes="bg-blue-400 aspect-square"):
      pass
    with me.box(classes="bg-blue-500 aspect-square"):
      pass
    with me.box(classes="bg-blue-600 aspect-square"):
      pass
    with me.box(classes="bg-blue-700 aspect-square"):
      pass
    with me.box(classes="bg-blue-800 aspect-square"):
      pass
    with me.box(classes="bg-blue-900 aspect-square"):
      pass

  with me.box(classes="grid grid-cols-10 gap-2"):
    with me.box(classes="bg-indigo-50 aspect-square"):
      pass
    with me.box(classes="bg-indigo-100 aspect-square"):
      pass
    with me.box(classes="bg-indigo-200 aspect-square"):
      pass
    with me.box(classes="bg-indigo-300 aspect-square"):
      pass
    with me.box(classes="bg-indigo-400 aspect-square"):
      pass
    with me.box(classes="bg-indigo-500 aspect-square"):
      pass
    with me.box(classes="bg-indigo-600 aspect-square"):
      pass
    with me.box(classes="bg-indigo-700 aspect-square"):
      pass
    with me.box(classes="bg-indigo-800 aspect-square"):
      pass
    with me.box(classes="bg-indigo-900 aspect-square"):
      pass

  with me.box(classes="grid grid-cols-10 gap-2"):
    with me.box(classes="bg-violet-50 aspect-square"):
      pass
    with me.box(classes="bg-violet-100 aspect-square"):
      pass
    with me.box(classes="bg-violet-200 aspect-square"):
      pass
    with me.box(classes="bg-violet-300 aspect-square"):
      pass
    with me.box(classes="bg-violet-400 aspect-square"):
      pass
    with me.box(classes="bg-violet-500 aspect-square"):
      pass
    with me.box(classes="bg-violet-600 aspect-square"):
      pass
    with me.box(classes="bg-violet-700 aspect-square"):
      pass
    with me.box(classes="bg-violet-800 aspect-square"):
      pass
    with me.box(classes="bg-violet-900 aspect-square"):
      pass
