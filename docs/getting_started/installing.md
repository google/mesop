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
