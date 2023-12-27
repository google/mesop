"""
This file generates all the boilerplate, but it's not idempotent (e.g. running it multiple times isn't good).

Run from the root of the repo:
python scripts/scaffold_component.py $component_name
"""
import argparse
import os
import shutil

parser = argparse.ArgumentParser(description="Process a single CLI argument.")
parser.add_argument(
  "component_name", type=str, help="The CLI argument to process"
)

args = parser.parse_args()

component_name = args.component_name


def main():
  print("Start generating new component: " + component_name)

  # Copy template directory
  shutil.copytree(
    os.path.join(current_dir(), "component_template"),
    new_component_dir(),
  )

  # Rename & update new component files
  rename_and_update_file(".py")
  rename_and_update_file(".ts")
  rename_file(".ng.html")
  rename_and_update_file(".proto")
  replace_component_name_ref(
    path=rename_file(".py", filename_suffix="_app", dir="e2e"),
  )
  replace_component_name_ref(
    path=rename_file(".ts", filename_suffix="_test", dir="e2e"),
  )

  # Update e2e init file
  replace_component_name_ref(
    path=os.path.join(new_component_dir(), "e2e", "__init__.py"),
  )

  # Update component BUILD file
  replace_component_name_ref(
    path=os.path.join(new_component_dir(), "BUILD"),
  )

  # Update //mesop/__init__.py
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "__init__.py"),
    target="# REF(//scripts/scaffold_component.py):insert_component_import_export",
    content=f"from mesop.components.{component_name}.{component_name} import {component_name} as {component_name}",
    before=True,
  )

  # Update //mesop/BUILD
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "BUILD"),
    target="# REF(//scripts/scaffold_component.py):insert_component_import",
    content=f'    "//mesop/components/{component_name}:py",',
  )

  # Update examples BUILD file
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "examples", "BUILD"),
    target="# REF(//scripts/scaffold_component.py):insert_component_e2e_import",
    content=f'    "//mesop/components/{component_name}/e2e",',
  )

  # Update examples example_index.py file
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "example_index.py"),
    target="# REF(//scripts/scaffold_component.py):insert_component_e2e_import_export",
    content=f"import mesop.components.{component_name}.e2e as {component_name}_e2e",
    before=True,
  )

  update_type_to_components_ts()

  print("Finished generating new component: " + component_name)


def update_type_to_components_ts():
  component_renderer_path = os.path.join(web_src_dir(), "component_renderer")

  update_file(
    path=os.path.join(component_renderer_path, "BUILD"),
    target="# REF(//scripts/scaffold_component.py):insert_component_import",
    content=f'    "//mesop/components/{component_name}:ng",',
  )

  ts_path = os.path.join(component_renderer_path, "type_to_component.ts")
  update_file(
    path=ts_path,
    content=f'import {{ {camel_case()}Component }} from "../../../components/{component_name}/{component_name}";',
  )

  update_file(
    path=ts_path,
    target="export const typeToComponent = {",
    content=f"    '{component_name}': {camel_case()}Component,",
  )


##################
# UTILITIES
##################


def update_file(
  path: str, content: str, target: str | None = None, before: bool = False
):
  with open(path) as f:
    lines = f.readlines()

  if target is None:
    lines.insert(0, content + "\n")
  else:
    for i in range(len(lines)):
      if target and target in lines[i]:
        lines.insert(i + (0 if before else 1), content + "\n")
        break

  with open(path, "w") as f:
    f.writelines(lines)


def camel_case():
  """
  Split underscore and make it UpperCamelCase
  """
  return "".join(x.title() for x in component_name.split("_"))


def kebab_case():
  """
  Split underscore and make it kebab-case
  """
  return "-".join(x for x in component_name.split("_"))


def rename_and_update_file(extension: str):
  replace_component_name_ref(path=rename_file(extension))


def replace_component_name_ref(path: str):
  with open(path) as f:
    lines = f.readlines()

  for i in range(len(lines)):
    lines[i] = (
      lines[i]
      .replace("{component_name}", component_name)
      .replace("{component-name}", kebab_case())
      .replace("ComponentName", camel_case())
      .replace("component_name", component_name)
    )

  with open(path, "w") as f:
    f.writelines(lines)


def rename_file(
  extension: str, filename_suffix: str = "", dir: str = ""
) -> str:
  dst_dir = new_component_dir()
  new_file_path = os.path.join(
    dst_dir, dir, component_name + filename_suffix + extension
  )
  os.rename(
    os.path.join(dst_dir, dir, "component_name" + filename_suffix + extension),
    new_file_path,
  )
  return new_file_path


def web_src_dir():
  return os.path.join(
    current_dir(),
    "..",
    "mesop",
    "web",
    "src",
  )


def current_dir():
  return os.path.dirname(os.path.realpath(__file__))


def new_component_dir():
  return os.path.join(
    current_dir(), "..", "mesop", "components", component_name
  )


if __name__ == "__main__":
  main()
