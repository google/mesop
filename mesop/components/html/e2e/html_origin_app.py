import mesop as me


@me.page(path="/components/html/e2e/html_origin_app")
def app():
  me.html(
    """<body>
      <script>document.body.innerHTML="origin: " + window.location.origin</script>
      </body>""",
    mode="sandboxed",
  )
