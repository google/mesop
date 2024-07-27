import mesop as me


@me.page(
  path="/testing/csp_escaping",
  title="Stress test CSP escaping",
  stylesheets=["http://google.com/stylesheets,1;2?q=a"],
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=[
      "http://google.com/allowed_iframe_parents/1,1;2?q=a",
      "http://google.com/allowed_iframe_parents/2,1;2?q=a",
    ],
    allowed_connect_srcs=[
      "http://google.com/allowed_connect_srcs/1,1;2?q=a",
      "http://google.com/allowed_connect_srcs/2,1;2?q=a",
    ],
    allowed_script_srcs=[
      "http://google.com/allowed_script_srcs/1,1;2?q=a",
      "http://google.com/allowed_script_srcs/2,1;2?q=a",
    ],
  ),
)
def page():
  me.text("CSP escaping")
