import mesop as me


@me.page(path="/components/html/e2e/html_app")
def app():
  s = me.state(State)

  me.text("Sanitized HTML")
  me.html(
    """
Custom HTML
<a href="https://google.github.io/mesop/" target="_blank">mesop</a>
""",
    mode="sanitized",
  )
  with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=24))):
    me.divider()
  me.text("Sandboxed HTML")
  me.html(
    """
           <!DOCTYPE html>
        <html>
        <head>
            <style>
                p {
                    color: blue;
                    font-size: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <p>I'm a big, blue, <strong>strong</strong> paragraph</p>
            <table>
                <tr><th>First_Name</th><th>Last_Name</th><th>Marks</th></tr>
                <tr><td>Sonoo</td><td>MURUGAN</td><td>38</td></tr>
                <tr><td>James</td><td>William</td><td>80</td></tr>
                <tr><td>Swati</td><td>Sironi</td><td>82</td></tr>
                <tr><td>Chetna</td><td>Singh</td><td>72</td></tr>
            </table>
        </body>
        </html>
          """,
    mode="sandboxed",
  )
  me.button("Increment sandboxed HTML", on_click=increment_sandboxed_html)
  me.html(
    f"iamsandboxed-{s.counter}<script>console.log('iamsandboxed-{s.counter}'); </script>",
    mode="sandboxed",
  )


@me.stateclass
class State:
  counter: int


def increment_sandboxed_html(e: me.ClickEvent):
  s = me.state(State)
  s.counter += 1
