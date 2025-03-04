# Publishing

Follow these instructions for releasing a new version of Mesop publicly via PyPI (e.g. `pip install mesop`).

## Check main branch

Before, cutting a release, you'll want to check two things:

1. The `main` branch should be healthy (e.g. latest commit is green).
2. Check the [snyk dashboard](https://app.snyk.io/org/wwwillchen/project/756c376f-d2e7-44f8-9c20-e4062fdf543f) to review security issues:

    - It only runs weekly so you need to click "Retest now". If there's any High security issues for a core Mesop file (e.g. anything in `mesop/*`), then you should address it before publishing a release.

## Update version to RC

Update [`mesop/version.py`](https://github.com/google/mesop/blob/main/mesop/version.py) by incrementing the version number. We follow semver.

You want to first create an RC (release candidate) to ensure that it works.

For example, if the current version is: `0.7.0`, then you should increment the version to `0.8.0rc1` which will create an RC, which is treated as a [pre-release by PyPI](https://packaging.python.org/en/latest/specifications/version-specifiers/#pre-releases).

Merge the PR that bumps the version and then go to the next step to publish a GitHub release which will in turn publish to PyPI.

## Publish GitHub release

After you've submitted the PR which bumps the version and then [publish a GitHub release](https://github.com/google/mesop/releases/new).

1. Click "Choose a tag" and type in the version you just released. This will create a new Git tag.
1. Click "Generate release notes".
1. **If this is a an RC:** Click "Set as a pre-release", **otherwise** leave the "Set as the latest release" checked.
1. If this is a regular (non-RC) release, click "Create a discussion for this release".
1. Click "Publish release".

## Testing locally

**Pre-requisite:** you will need to [install uv](https://docs.astral.sh/uv/getting-started/installation/) before doing the following steps.

### Dev CLI

Run the following command but replace `0.1.0rc1` with the version that you just published:

```sh
uvx mesop==0.1.0rc1 scripts/smoketest_app/main.py
```

This will start the Mesop dev server and you can test that hot reload works. Double-check that the version shown is the version that you just released.

### Gunicorn integration

Run the following command but replace `0.1.0rc1` with the version that you just published:

```sh
cd scripts/smoketest_app/ && uvx --with mesop==0.1.0rc1 gunicorn@latest main:me
```

This will launch Mesop under the Gunicorn server so you can make sure it works as expected.

## Test on Colab

Because Colab installs from PyPI, you will need to test the RC on Colab after uploading to PyPI.

Open our [Mesop Colab notebook](https://colab.research.google.com/github/google/mesop/blob/main/notebooks/mesop_colab_getting_started.ipynb). You will need to explicitly pip install the RC version as pip will _not_ automatically install a pre-release version, even if it's the newest version. So change the first cell to something like:

```sh
 !pip install mesop==0.X.Yrc1
```

> Tip: sometimes it takes a minute for the PyPI registry to be updated after upload, so just try again.

Then, run all the cells and make sure it works. Usually if something breaks in Colab, it's pretty obvious because the output isn't displayed, etc.

## Change the version from RC to regular release

If you find an issue, then redo the above steps and create another RC candidate: `0.8.0rc1` -> `0.8.0rc2`.

If all the testing looks good, then you can update [`mesop/version.py`](https://github.com/google/mesop/blob/main/mesop/version.py) and change the version from RC to a regular release, for example:

`0.8.0rc1` -> `0.8.0`

Re-do the steps above to publish and test the release.
