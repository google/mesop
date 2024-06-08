# Installing

If you are familiar with setting up a Python environment, then run the following command in your terminal:

```shell
$ pip install mesop
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

1. In the terminal, navigate to your project directory: `cd foo`

2. Use [venv](https://docs.python.org/3/library/venv.html) to create a virtual environment, which will help avoid many of the common Python environment issues. Run:

```sh
python -m venv .venv
```

3. Active your virtual environment:

    - macOS and Linux:

        ```sh
        source .venv/bin/activate
        ```

    - Windows command prompt:

        ```sh
        .venv\Scripts\activate.bat
        ```

    - Windows PowerShell

        ```sh
        .venv\Scripts\Activate.ps1
        ```

Once you've activated the virtual environment, you will see ".venv" at the start of your terminal prompt.

Make sure your Python environment is setup correctly by running a hello world app.

Copy the following hello world code into a file `hello_world.py`:

```python title="hello_world.py"
import mesop as me


@me.page()
def app():
  me.text("Hello World")
```

Then run the following command in your terminal:

```shell
$ mesop hello_world.py
```

Open the URL printed in the terminal (i.e. http://localhost:32123) in the browser to see your Mesop app loaded.

If you make changes to the code (e.g. change `"Hello World"` to `"Hi"`), the Mesop app should be automatically hot reloaded.
