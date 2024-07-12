def colab_show(
  port: int = 32123, path: str = "/", width: str = "100%", height: str = "400"
):
  """
  Displays Mesop app in a Colab cell output.
  """
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
  """Displays the Mesop app in a JupyterLab cell output as an IFrame."""
  from IPython.display import IFrame, display

  display(
    IFrame(src=f"http://localhost:{port}{path}", width=width, height=height)
  )
