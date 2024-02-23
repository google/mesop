# Deployment

To deploy your Mesop application, we recommend using [Google Cloud Run](https://cloud.google.com/run) because it's easy to get started and there's a [free tier](https://cloud.google.com/run#pricing). However, it's possible to deploy your Mesop to other Cloud platforms.

## Example application

### Python

`main.py` which is your Mesop application code:

``` py title="main.py"
import mesop as me

@me.page(title="Home")
def home():
  me.text("Hello, world")
```

> Note: if you choose to use a different filename than main.py, you will need to modify the `Procfile` below.

### Procfile

`Procfile` which configures `gunicorn` to run Mesop.

```title="Procfile"
web: gunicorn --bind :8080 main:me
```

The `--bind: 8080` will run Mesop on port 8080.

The `main:me` syntax is `$(MODULE_NAME):$(VARIABLE_NAME)`: (see [Gunicorn docs](https://docs.gunicorn.org/en/stable/run.html) for more details):

 - Because the Mesop python file is `main.py`, the module name is `main`.
 - By convention, we do `import mesop as me` so the `me` refers to the main Mesop library module which is also a callable (e.g. a function) that conforms to WSGI.

### requirements.txt

`requirements.txt` specifies the Python dependencies needed. You may need to add additional dependencies depending on your use case.

```title="requirements.txt"
mesop
Flask==3.0.0
gunicorn==20.1.0
Werkzeug==3.0.1
```

## Pre-requisites

You will need to create a [Google Cloud](https://cloud.google.com/) account and install the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install).

## Deploy to Google Cloud Run

In your terminal, go to the application directory, which has the files listed above.

Run the following command:

```sh
$ gcloud run deploy
```

Follow the instructions and then you should be able to access your deployed app.
