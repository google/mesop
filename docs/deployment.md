# Deployment

If you want to deploy your Optic application, we recommend using a container (e.g. Docker) for simplicity.

## Build Container image

After cloning this repository and navigating to the repo root directory, run the following command.

### Remote (GCP)

These are instructions for using Google Cloud Build and Artifact Registry.

**Pre-requisite: Create Docker repo**:

Google Cloud Artifact Registry provides a private Docker repo.

You only need to run this once and then you can re-use the same repo for multiple builds.

* Follow Cloud Build's [Docker quickstart guide](https://cloud.google.com/build/docs/build-push-docker-image) for any pre-requisites.

```sh
gcloud artifacts repositories create {REPO_NAME} --repository-format=docker \
    --location=us-west2 --description="Optic app: Docker repository"
```

> NOTE: Keep in mind the location as you will be using it for the next step. Also, some locations do not support gcloud builds.

**Running Google Cloud Build**:

Google Cloud Build can create a container image based on a Dockerfile.

```sh
$ gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/optic-testing-404806/optic/optic:latest
```

> TIP: If you want to inspect/debug the container image, you can [pull the container image](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#get-image) and run it locally

### Local (Docker)

**Build local image**:

```sh
$ docker build -t {TAG_NAME} .
```

> NOTE: This isn't recommended because it takes a long time and frequently hangs unless you have a very well-provisioned machine / container.

**Deploy image to repo**:

```sh
$ docker push ${REPO_NAME}
```

> NOTE: you will need to create the docker repo before-hand.

## Deploying Container

There's many cloud providers and services that allow you to run a container. 

To help you get started, I will show one example using Google Cloud Run.

### Google Cloud Run

- Follow Cloud Run's [container deployment guide](https://cloud.google.com/run/docs/deploying) for general Cloud Run instructions.

**Tips:**

- Set the "Container image URL" to the container that you created in the previous step.
- Set "Container command" to `./bazel-bin/optic/cli`
- Set "Container arguments" to `--path=/optic/optic/examples/simple.py` (note: you should configure this to your application)
- Under Resources, set Memory to at least "1 GiB".

Once you deploy on Cloud Run, you should have a public URL for your application that will look something like: https://{APP_PREFIX}.run.app

## Debugging

### Run container locally

If you've finished building the container image, but you're having difficulty running it in a cloud environment, you can try running the container image locally:

```sh
$ docker run -p 8080:8080 --platform linux/amd64 -it optic  /bin/bash
```
