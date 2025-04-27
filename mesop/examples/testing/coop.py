import mesop as me


@me.page(
  path="/testing/coop_same_origin",
  title="COOP: Same Origin",
  security_policy=me.SecurityPolicy(
    cross_origin_opener_policy="same-origin",
  ),
)
def page_same_origin():
  me.text("COOP - Same Origin")


@me.page(
  path="/testing/coop_same_origin_allow_popups",
  title="COOP: Same Origin Allow Popups",
  security_policy=me.SecurityPolicy(
    cross_origin_opener_policy="same-origin-allow-popups",
  ),
)
def page_same_origin_allow_popups():
  me.text("COOP - Same Origin Allow Popups")


@me.page(
  path="/testing/coop_noopener_allow_popups",
  title="COOP: Noopener Allow Popups",
  security_policy=me.SecurityPolicy(
    cross_origin_opener_policy="noopener-allow-popups",
  ),
)
def page_noopener_allow_popups():
  me.text("COOP - Noopener Allow Popups")
