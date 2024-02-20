def log_startup(port: int):
  # Log basic information about where the server is running since
  # we don't get it printed by werkzeurg:
  # https://github.com/pallets/werkzeug/blob/eafbed0ce2a6bdf60e62de82bf4a8365188ac334/src/werkzeug/serving.py#L820C9-L820C17
  FgGreen = "\x1b[32m"
  Reset = "\x1b[0m"
  print(
    f"\n{FgGreen}Running server on: http://localhost:{port}{Reset}",
  )
