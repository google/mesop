import mesop as me


def on_load(e: me.LoadEvent):
  me.query_params["on_load"] = "loaded"


@me.page(path="/examples/query_params", on_load=on_load)
def page():
  me.text(f"query_params={me.query_params}")
  me.button("append query param list", on_click=append_query_param_list)
  me.button("URL-encoded query param", on_click=url_encoded_query_param)
  me.button(
    "navigate URL-encoded query param",
    on_click=navigate_url_encoded_query_param,
  )
  me.button("increment query param directly", on_click=increment_query_param)
  me.button("delete list query param", on_click=delete_list_query_param)
  me.button("delete all query params", on_click=delete_all_query_params)
  me.button("increment query param by navigate", on_click=increment_by_navigate)
  me.button("navigate to page 2 with query params", on_click=navigate_page_2)
  me.button("navigate to page 2 with dict", on_click=navigate_page_2_new_dict)
  me.button(
    "navigate to page 2 without query params",
    on_click=navigate_page_2_without_query_params,
  )


@me.stateclass
class State:
  click_append_query_param_list: int


def append_query_param_list(e: me.ClickEvent):
  current_list = (
    [] if "list" not in me.query_params else me.query_params.get_all("list")
  )
  state = me.state(State)
  state.click_append_query_param_list += 1
  me.query_params["list"] = [
    *current_list,
    f"val{state.click_append_query_param_list}",
  ]


def url_encoded_query_param(e: me.ClickEvent):
  me.query_params["url_encoded"] = ["&should-be-escaped=true"]


def navigate_url_encoded_query_param(e: me.ClickEvent):
  me.navigate(
    "/examples/query_params/page_2",
    query_params={
      "url_encoded": "&should-be-escaped=true",
      "url_encoded_values": ["value1&a=1", "value2&a=2"],
    },
  )


def increment_query_param(e: me.ClickEvent):
  if "counter" not in me.query_params:
    me.query_params["counter"] = "0"

  me.query_params["counter"] = str(int(me.query_params["counter"]) + 1)


def delete_list_query_param(e: me.ClickEvent):
  del me.query_params["list"]


def delete_all_query_params(e: me.ClickEvent):
  for key in list(me.query_params.keys()):
    del me.query_params[key]


def navigate_page_2(e: me.ClickEvent):
  me.navigate("/examples/query_params/page_2", query_params=me.query_params)


def navigate_page_2_new_dict(e: me.ClickEvent):
  me.navigate(
    "/examples/query_params/page_2",
    query_params={"page2": ["1", "2"], "single": "a"},
  )


def navigate_page_2_without_query_params(e: me.ClickEvent):
  me.navigate("/examples/query_params/page_2")


def increment_by_navigate(e: me.ClickEvent):
  if "counter" not in me.query_params:
    me.query_params["counter"] = "0"

  counter = int(me.query_params["counter"]) + 1
  me.query_params["counter"] = str(counter)

  me.navigate(
    "/examples/query_params",
    query_params=me.query_params,
  )


@me.page(path="/examples/query_params/page_2")
def page_2():
  me.text(f"query_params(page_2)={me.query_params}")
  me.button("Navigate back", on_click=navigate_back)
  me.button("Navigate page 3", on_click=navigate_page_3)


def on_load_page_3(e: me.LoadEvent):
  me.query_params["on_load_page_3"] = "loaded"


@me.page(path="/examples/query_params/page_3", on_load=on_load_page_3)
def page_3():
  me.text(f"query_params(page_3)={me.query_params}")


def navigate_back(e: me.ClickEvent):
  me.navigate("/examples/query_params", query_params=me.query_params)


def navigate_page_3(e: me.ClickEvent):
  me.navigate("/examples/query_params/page_3")
