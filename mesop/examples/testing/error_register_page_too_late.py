import mesop as me


@me.page(path="/testing/error_register_page_too_late")
def page():
  me.text("error_register_page_too_late")

  @me.page(path="/testing/error_register_page_too_late/too_late_page")
  def too_late_page():
    me.text("too_late_page")
