# Deployment

This section describes how to run your Mesop application using the following
platforms:

- [Google Cloud Run](#cloud-run)
- [Google App Engine](#app-engine)
- [Docker](#docker)

If you can run your Mesop app on [Docker](https://www.docker.com/), you should be able
to run it on many other cloud platforms as well.

## Example application

Let's start with an example application which will consist of the following files:

- main.py
- requirements.txt

### main.py

This file contains your Mesop application code:

```py title="main.py"
import mesop as me

@me.page(title="Home")
def home():
  me.text("Hello, world")
```

### requirements.txt

This file specifies the Python dependencies needed. You may need to add additional
dependencies depending on your use case.

```title="requirements.txt"
mesop
gunicorn
```

## Cloud Run

We recommend using [Google Cloud Run](https://cloud.google.com/run) because it's easy to
get started and there's a [free tier](https://cloud.google.com/run#pricing).

### Pre-requisites

You will need to create a [Google Cloud](https://cloud.google.com/) account and install the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install). See the official documentation for [detailed instructions](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service#before-you-begin).

### Procfile

Create `Procfile` to configure `gunicorn` to run Mesop.

```title="Procfile"
web: gunicorn --bind :8080 main:me
```

The `--bind: 8080` will run Mesop on port 8080.

The `main:me` syntax is `$(MODULE_NAME):$(VARIABLE_NAME)`: (see [Gunicorn docs](https://docs.gunicorn.org/en/stable/run.html) for more details):

 - Because the Mesop python file is `main.py`, the module name is `main`.
 - By convention, we do `import mesop as me` so the `me` refers to the main Mesop
   library module which is also a callable (e.g. a function) that conforms to WSGI.

### Deploy to Google Cloud Run

In your terminal, go to the application directory, which has the files listed above.

Run the following command:

```sh
gcloud run deploy
```

Follow the instructions and then you should be able to access your deployed app.

## App Engine

This section describes deployment to [Google App Engine](https://cloud.google.com/appengine) using
their [flexible environments](https://cloud.google.com/appengine/docs/flexible) feature.

### Pre-requisites

You will need to create a [Google Cloud](https://cloud.google.com/) account and install the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install). See the official documentation for [detailed instructions](https://cloud.google.com/appengine/docs/flexible/python/create-app#before-you-begin).

You will also need to run:

```sh
gcloud app create --project=[YOUR_PROJECT_ID]
gcloud components install app-engine-python
```

### app.yaml

Create `app.yaml` to configure App Engine to run Mesop.

```yaml title="app.yaml"
runtime: python
env: flex
entrypoint: gunicorn -b :$PORT main:me

runtime_config:
  operating_system: ubuntu22
  runtime_version: "3.10"

manual_scaling:
  instances: 1

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10
```

### Deploy to App Engine

In your terminal, go to the application directory, which has the files listed above.

Run the following command:

```sh
gcloud app deploy
```

Follow the instructions and then you should be able to access your deployed app.

## Docker

If you can run your Mesop app on [Docker](https://www.docker.com/), you should be able
to run it on many other cloud platforms.

### Pre-requisites

Make sure [Docker and Docker Compose are installed](https://docs.docker.com/engine/install/).

### Dockerfile

```Docker title="Dockerfile"
FROM python:3.10.14-bullseye

RUN apt-get update && \
  apt-get install -y \
  # General dependencies
  locales \
  locales-all && \
  # Clean local repository of package files since they won't be needed anymore.
  # Make sure this line is called after all apt-get update/install commands have
  # run.
  apt-get clean && \
  # Also delete the index files which we also don't need anymore.
  rm -rf /var/lib/apt/lists/*

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create non-root user
RUN groupadd -g 900 mesop && useradd -u 900 -s /bin/bash -g mesop mesop
USER mesop

# Add app code here
COPY . /srv/mesop-app
WORKDIR /srv/mesop-app

# Run Mesop through gunicorn. Should be available at localhost:8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:me"]
```

### docker-compose.yaml

```title="docker-compose.yaml"
services:
  mesop-app:
    build: .
    ports:
      - "8080:8080"
```

### Run Docker image

In your terminal, go to the application directory, which has the files listed above.

Run the following command:

```sh
docker-compose up -d
```

Alternatively, if you do not want to use Docker Compose, you can run:

```sh
docker build -t mesop-app . && docker run -d -p 8080:8080 mesop-app
```

You should now be able to view your Mesop app at http://localhost:8080.
