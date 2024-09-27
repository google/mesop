import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  stylesheets=[
    "/assets/bootstrap.css",
  ],
  path="/bootstrap",
)
def page():
  with me.box(classes="container"):
    with me.box(
      classes="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom",
    ):
      with me.box(
        classes="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none fs-4",
      ):
        me.text("Mesop")

      with me.box(classes="nav nav-pills"):
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link active"):
            me.text("Pricing")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link"):
            me.text("Features")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link"):
            me.text("About")

  with me.box(classes="container px-4 py-5"):
    with me.box(classes="pb-2 border-bottom"):
      me.text("Columns", type="headline-5")

    with me.box(classes="row g-4 py-5 row-cols-1 row-cols-lg-3"):
      with me.box(classes="feature col"):
        with me.box(classes="fs-2 text-body-emphasis"):
          me.text("Featured title")
        me.text(
          "Paragraph of text beneath the heading to explain the heading. We'll add onto it with another sentence and probably just keep going until we run out of words."
        )
        me.link(text="Call to action", url="/#")

      with me.box(classes="feature col"):
        with me.box(classes="fs-2 text-body-emphasis"):
          me.text("Featured title")
        me.text(
          "Paragraph of text beneath the heading to explain the heading. We'll add onto it with another sentence and probably just keep going until we run out of words."
        )
        me.link(text="Call to action", url="/#")

      with me.box(classes="feature col"):
        with me.box(classes="fs-2 text-body-emphasis"):
          me.text("Featured title")
        me.text(
          "Paragraph of text beneath the heading to explain the heading. We'll add onto it with another sentence and probably just keep going until we run out of words."
        )
        me.link(text="Call to action", url="/#")

    with me.box(
      classes="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top"
    ):
      with me.box(classes="col-md-4 mb-0 text-body-secondary"):
        me.text("Copyright 2024 Mesop")

      with me.box(
        classes="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none"
      ):
        me.icon("home")

      with me.box(classes="nav col-md-4 justify-content-end"):
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link px-2 text-body-secondary"):
            me.text("Home")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link px-2 text-body-secondary"):
            me.text("Features")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link px-2 text-body-secondary"):
            me.text("Pricing")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link px-2 text-body-secondary"):
            me.text("FAQs")
        with me.box(classes="nav-item"):
          with me.box(classes="nav-link px-2 text-body-secondary"):
            me.text("About")
