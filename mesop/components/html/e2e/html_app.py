import mesop as me


@me.page(path="/components/html/e2e/html_app")
def app():
  me.html(
    """
Custom HTML
<a href="https://google.github.io/mesop/" target="_blank">mesoplink</a>
"""
  )
