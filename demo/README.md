---
title: Mesop Demo Gallery
emoji: 👓
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: apache-2.0
app_port: 8080
---

# Mesop demo app

This app demonstrates Mesop's various components and features. Create your own Cloud Run app by following: https://google.github.io/mesop/guides/deployment/

## Development

### Setup

From workspace root:

```sh
rm -rf demo/venv && \
virtualenv --python python3 demo/venv && \
source demo/venv/bin/activate && \
pip install -r demo/requirements.txt
```

### Run

1. `cd demo`
1. `mesop main.py`

## Generate screenshots

If you add more demos and want to re-generate screenshots, do the following steps:

1. in `demo/screenshot.ts` change `test.skip` to `test`
1. Run: `yarn playwright test demo/screenshot.ts`
1. Install cwebp using `brew install webp` or download from [here](https://developers.google.com/speed/webp/docs/precompiled).
1. From the workspace root, run:

```sh
`for file in demo/screenshots/*; do cwebp -q 50 "$file" -o "${file%.*}.webp"; done`
```

## Deployment

**Pre-requisites:**

- Make sure you [generate screenshots](#generate-screenshots) before deploying!
- Ensure a recent version of Mesop has been published to pip, otherwise the demos may not work (because they rely on a new API).

### Deploy to Cloud Run

This app is deployed to Google Cloud Run.

```sh
gcloud run deploy mesop --source .
```

See our Mesop deployment [docs](https://google.github.io/mesop/guides/deployment/#deploy-to-google-cloud-run) for more background.

### Deploy to Hugging Face Spaces

> NOTE: You need to update demo/requirements.txt to point to the latest Mesop version because Hugging Face Spaces may use a cached version of Mesop which is too old.

Because Hugging Face Spaces has restrictions on not having binary files (e.g. image files), we cannot push the full Mesop Git repo to Hugging Face Spaces. Instead, we copy just the `demo` directory and turn it into a standalone Git repo which we deploy.

```sh
./demo/deploy_to_hf.sh ../hf_demo
```

You can change `../hf_demo` to any dir path outside of your Mesop repo.

> Note: if you get an error in Hugging Face Spaces "No app file", then you can create an "app.py" file in the Spaces UI to manually trigger a build. This seems like a bug with Hugging Face.
