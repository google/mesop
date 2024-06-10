import mesop as me


@me.page(path="/components/embed/e2e/embed_html_app")
def app():
  me.embed(
    html="<script>document.body.innerHTML='hi';</script>",
    style=me.Style(width="100%", height="100%"),
  )
