import mesop as me


@me.page(path="/components/html/e2e/html_default_app")
def app():
  me.html("i am <a href='#'>sanitized</a>")
  me.html(
    """<body><script>document.body.innerHTML='iamsandboxed'</script></body>"""
  )
