# Server integration

Mesop allows you to integrate Mesop with other Python web servers like FastAPI or Flask by mounting the Mesop app which is a [WSGI](https://wsgi.readthedocs.io/en/latest/what.html) app.

This enables you to do things like:

- Serve local files (e.g. images)
- Provide API endpoints (which can be called by the web component, etc.)

## API

The main API for doing this integration is the `create_wsgi_app` function.

::: mesop.server.wsgi_app.create_wsgi_app

## FastAPI example

For a working example of using Mesop with FastAPI, please take a look at this repo:
[https://github.com/wwwillchen/mesop-fastapi](https://github.com/wwwillchen/mesop-fastapi)

> Note: you can apply similar steps to use any other web framework that allows you to mount a WSGI app.
