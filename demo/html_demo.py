import mesop as me


@me.page(path="/html_demo")
def app():
  me.html(
    """
Custom HTML
<a href="https://google.github.io/mesop/" target="_blank">mesop</a>
"""
  )
