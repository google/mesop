from flask import Flask, Response


def configure_dev_server(app: Flask):
  # Disable CORS for development purpose since FE dev server is on a separate origin
  # from this server.
  @app.after_request
  def after_request(response: Response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization"
    )
    response.headers.add(
      "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response
