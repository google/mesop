import base64
import os
import re
import secrets
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable

from absl import flags
from flask import Flask, request

from mesop.cli.execute_module import execute_module
from mesop.runtime import (
  enable_debug_mode,
)
from mesop.server.constants import PROD_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving

PAGE_EXPIRATION_MINUTES = 10
MAIN_MODULE = "main"


@dataclass(frozen=True)
class RegisteredModule:
  name: str = ""
  created_at: datetime = field(default_factory=lambda: datetime.now())


registered_modules = set([RegisteredModule(MAIN_MODULE)])


class App:
  _flask_app: Flask

  def __init__(self, flask_app: Flask):
    self._flask_app = flask_app

  def run(self):
    log_startup(port=port())
    self._flask_app.run(host="::", port=port(), use_reloader=False)


counter = 0


def create_app(
  prod_mode: bool, run_block: Callable[..., None] | None = None
) -> App:
  flask_app = configure_flask_app(prod_mode=prod_mode)

  # Enable debug mode so we can see errors with the code we're running.
  enable_debug_mode()

  if run_block is not None:
    run_block()

  configure_static_file_serving(
    flask_app, static_file_runfiles_base=PROD_PACKAGE_PATH
  )

  @flask_app.route("/exec-py", methods=["POST"])
  def exec_py_route():
    global counter
    param = request.form.get("code")
    if param is None:
      raise Exception("Missing request parameter")
    code = base64.urlsafe_b64decode(param)
    module_name = f"temp_module_{counter}"
    with open(f"{module_name}.py", "w") as file:
      file.write(code.decode("utf-8"))
    try:
      execute_module(
        module_path=make_path_absolute(f"{module_name}.py"),
        module_name=module_name,
      )
    except Exception as e:
      return str(e), 500
    counter += 1
    return "OK"

  @flask_app.route("/exec", methods=["POST"])
  def exec_route():
    global registered_modules
    print("Entering exec_route")

    param = request.form.get("code")
    new_module = RegisteredModule()
    if param is None:
      print("Error: Missing request parameter")
      raise Exception("Missing request parameter")
    try:
      new_module = RegisteredModule(f"page_{secrets.token_urlsafe(8)}")
      print(f"Created new module: {new_module.name}")

      # Create a new page with the code to run
      code = base64.urlsafe_b64decode(param)
      code = code.decode("utf-8")
      # Remove security policy as we will repliace it with ours
      code = re.sub(
        r"security_policy=me\.SecurityPolicy\([^)]*\),?\s*",
        "",
        code,
        flags=re.DOTALL,
      )
      path_match = re.search(r'path="([^"]+)"', code)
      if path_match:
        path = path_match.group(1)
        code = code.replace(f'path="{path}"', f'path="/{new_module.name}"')
        # Remove security_policy parameter if present
        code = code.replace(
          "@me.page(",
          '@me.page(security_policy=me.SecurityPolicy(allowed_iframe_parents=["localhost:*"]),',
        )
      else:
        code = code.replace(
          "@me.page(",
          f'@me.page(path="/{new_module.name}", security_policy=me.SecurityPolicy(allowed_iframe_parents=["localhost:*"]),',
        )
      print(f"Code: {code}")
      with open(f"{new_module.name}.py", "w") as file:
        file.write(code)

      # Add new registered path
      registered_modules.add(new_module)

      print(f"Added new registered path: {new_module.name}")
      print(f"Total registered modules: {len(registered_modules)}")

      # Clean up old registered paths (except main)
      registered_modules_to_delete = set()
      for registered_module in registered_modules:
        if (
          registered_module.name != MAIN_MODULE
          and registered_module.name != new_module.name
        ):
          registered_modules_to_delete.add(registered_module)
      print(f"Registered modules to delete: {registered_modules_to_delete}")
      registered_modules -= registered_modules_to_delete

      for module in registered_modules:
        print(f"Executing module: {module.name}")
        execute_module(
          module_path=make_path_absolute(f"{module.name}.py"),
          module_name=module.name,
        )

    except Exception as e:
      print(f"Error occurred: {e!s}")
      exc_type, exc_value, exc_traceback = sys.exc_info()
      tb_string = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
      )
      return tb_string, 500

    print(f"Returning new module path: /{new_module.name}")
    return f"/{new_module.name}"

  return App(flask_app=flask_app)


_app = None

print("Starting WSGI app")


def wsgi_app(environ: dict[Any, Any], start_response: Callable[..., Any]):
  global _app
  if not _app:
    flags.FLAGS(sys.argv[:1])
    _app = create_app(prod_mode=True)
  return _app._flask_app.wsgi_app(environ, start_response)


def make_path_absolute(file_path: str):
  if os.path.isabs(file_path):
    return file_path
  absolute_path = os.path.join(os.getcwd(), file_path)
  return absolute_path
