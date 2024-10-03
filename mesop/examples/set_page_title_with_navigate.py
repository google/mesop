import mesop as me


@me.page(path="/set_page_title/page1")
def page1():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    with me.box(
      style=me.Style(display="flex", gap=15, margin=me.Margin(bottom=15))
    ):
      me.button(
        "set title",
        on_click=set_title,
        type="flat",
      )

      me.button(
        "title does not change if clicked",
        on_click=noop,
        type="flat",
      )

    me.text("Separate Yield", type="headline-5")

    with me.box(
      style=me.Style(display="flex", gap=15, margin=me.Margin(top=15))
    ):
      me.button(
        "title change before navigate",
        on_click=title_change_before_navigate,
        type="flat",
      )
      me.button(
        "title change after navigate",
        on_click=title_change_after_navigate,
        type="flat",
      )

  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("Grouped Yield", type="headline-5")

    with me.box(
      style=me.Style(display="flex", gap=15, margin=me.Margin(top=15))
    ):
      me.button(
        "(grouped) title change before navigate",
        on_click=grouped_title_change_before_navigate,
        type="flat",
      )
      me.button(
        "(grouped) title change after navigate",
        on_click=grouped_title_change_after_navigate,
        type="flat",
      )

  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("Multiple Yields", type="headline-5")

    with me.box(
      style=me.Style(display="flex", gap=15, margin=me.Margin(top=15))
    ):
      me.button(
        "(multi) title change before navigate",
        on_click=multi_yield_title_change_before_navigate,
        type="flat",
      )
      me.button(
        "(multi) title change after navigate",
        on_click=multi_yield_title_change_after_navigate,
        type="flat",
      )


@me.page(path="/set_page_title/page2")
def page2():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("page2")


@me.page(path="/set_page_title/page3")
def page3():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("page3")


def set_title(e: me.ClickEvent):
  me.set_page_title("Set title page 1")


def noop(e: me.ClickEvent):
  pass


def title_change_before_navigate(e: me.ClickEvent):
  me.set_page_title("Set Page 1")
  yield

  me.navigate("/set_page_title/page2")
  yield


def title_change_after_navigate(e: me.ClickEvent):
  me.navigate("/set_page_title/page2")
  yield

  me.set_page_title("Set Page 2")
  yield


def grouped_title_change_before_navigate(e: me.ClickEvent):
  me.set_page_title("set Page 1")
  me.navigate("/set_page_title/page2")
  yield


def grouped_title_change_after_navigate(e: me.ClickEvent):
  me.navigate("/set_page_title/page2")
  me.set_page_title("Set Page 2")
  yield


def multi_yield_title_change_before_navigate(e: me.ClickEvent):
  me.set_page_title("set Page 1")
  me.navigate("/set_page_title/page2")
  yield

  me.set_page_title("set Page 1")
  me.navigate("/set_page_title/page3")
  yield

  yield


def multi_yield_title_change_after_navigate(e: me.ClickEvent):
  me.navigate("/set_page_title/page2")
  me.set_page_title("Set Page 2")
  yield

  me.navigate("/set_page_title/page3")
  me.set_page_title("Set Page 3")
  yield

  yield
