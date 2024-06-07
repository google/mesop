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

## Generate screenshots

If you add more demos and want to re-generate screenshots, do the following steps:

1. in `demo/screenshot.ts` change `test.skip` to `test`
1. Run: `yarn playwright test demo/screenshot.ts`
1. Install cwebp using `brew install webp` or download from [here](https://developers.google.com/speed/webp/docs/precompiled).
1. From the workspace root, run:

```sh
`for file in demo/screenshots/*; do cwebp -q 50 "$file" -o "${file%.*}.webp"; done`
```
