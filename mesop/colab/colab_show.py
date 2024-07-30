from mesop.utils import colab_utils


def colab_show(
  port: int = 32123, path: str = "/", width: str = "100%", height: str = "400"
):
  """
  Displays Mesop app in a Colab cell output.
  """
  if not colab_utils.is_running_in_colab():
    print("Not running Colab: `colab_show` is a no-op")
    return

  # Intentionally import inside the function because the colab
  # package is only available in some environments that Mesop runs in.
  from google.colab import output  # type: ignore

  output.serve_kernel_port_as_iframe(  # type: ignore
    port=port,
    path=path,
    width=width,
    height=height,
  )


def notebook_show(
  port: int = 32123, path: str = "/", width: str = "100%", height: str = "400"
):
  """Displays the Mesop app in a notebook cell output as an IFrame.

  Use this for non-Colab notebook environments like Jupyter/JupyterLab.
  """
  if not colab_utils.is_running_ipython():
    print("Not running in a notebook environment: `notebook_show` is a no-op")
    return

  from IPython.display import IFrame, display  # type: ignore

  display(
    IFrame(src=f"http://localhost:{port}{path}", width=width, height=height)
  )
