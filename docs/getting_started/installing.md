# Installing

If you are familiar with setting up a Python environment, then run the following command in your terminal:

```shell
pip install mesop
```

If you're not familiar with setting up a Python environment, follow one of the options below.

## A. Colab (Recommended for beginners)

Colab is a free hosted Jupyter notebook product provided by Google.

Try Mesop on Colab: [![Open In Colab](../assets/colab.svg)](https://colab.research.google.com/github/google/mesop/blob/main/notebooks/mesop_colab_getting_started.ipynb)

## B. Command-line

If you'd like to run Mesop locally on the command-line, follow these steps.

**Pre-requisites:** Make sure you have Python version 3.10 or later installed by running:

```sh
python --version
```

If you don't, please [download Python](https://www.python.org/downloads/).

## C. IDX

If you want an IDE _without_ having to set-up your own local Python environment, then IDX is a good option for having a free cloud-based IDE:

<a href="https://idx.google.com/new?template=https%3A%2F%2Fgithub.com%2Fgoogle%2Fmesop%2Ftree%2Fidx%2Fidx%2F">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://cdn.idx.dev/btn/try_dark_32.svg">
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://cdn.idx.dev/btn/try_light_32.svg">
    <img
      height="32"
      alt="Try in IDX"
      src="https://cdn.idx.dev/btn/try_purple_32.svg">
  </picture>
</a>

???+ tip "Tips for setting up IDX"

    You will need to wait a minute or two for the IDX workspace to setup. Wait until the preview (web browser) opens with the Mesop app.

    If your workspace doesn't setup correctly, try again and create another IDX workspace.


### Create a venv environment

1. **Open the terminal** and navigate to a directory: `cd foo`

2. **Create a virtual environment** by using [venv](https://docs.python.org/3/library/venv.html), which will avoid Python environment issues. Run:

```sh
python -m venv .venv
```

3. **Activate your virtual environment:**

    === "macOS and Linux"

        ```sh
        source .venv/bin/activate
        ```

    === "Windows command prompt"

        ```sh
        .venv\Scripts\activate.bat
        ```

    === "Windows PowerShell"

        ```sh
        .venv\Scripts\Activate.ps1
        ```

Once you've activated the virtual environment, you will see ".venv" at the start of your terminal prompt.

4. **Install mesop:**

```shell
pip install mesop
```

## Next steps

Follow the quickstart guide to learn how to create and run a Mesop app:

<a href="../quickstart" class="next-step">
    Quickstart
</a>
