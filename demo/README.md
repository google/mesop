# Mesop demo app

This app demonstrates Mesop's various components and features. Create your own Cloud Run app by following: https://google.github.io/mesop/guides/deployment/

## Development

### Setup

From workspace root:

```sh
rm -rf demo/venv && \
virtualenv --python python3 demo/venv && \
source demo/venv/bin/activate && \
pip install -r demo/requirements.txt --no-binary pydantic
```

### Run

1. `cd demo`
1. `mesop main.py`

## Deployment

This app is deployed to Google Cloud Run.

```sh
$ gcloud run deploy mesop --source .
```

See our Mesop deployment [docs](https://google.github.io/mesop/guides/deployment/#deploy-to-google-cloud-run) for more background.
