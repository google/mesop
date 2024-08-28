import wsgi_app

import mesop as me

wsgi = wsgi_app.wsgi_app


@me.page(
  title="Mesop Sandbox Runner",
  security_policy=me.SecurityPolicy(allowed_iframe_parents=["localhost:*"]),
)
def main():
  me.text("Mesop Sandbox Runner")
