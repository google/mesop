"""
Run from the root of the repo:
python scripts/gen_component.py $component_name
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
    target="# REF(//scripts/gen_component.py):insert_component_import_export",
    content=f"from mesop.components.{component_name}.{component_name} import {component_name} as {component_name}",
    before=True,
  )

  # Update //mesop/BUILD
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "BUILD"),
    target="# REF(//scripts/gen_component.py):insert_component_import",
    content=f'    "//mesop/components/{component_name}:py",',
  )

  # Update testing BUILD file
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "testing", "BUILD"),
    target="# REF(//scripts/gen_component.py):insert_component_e2e_import",
    content=f'    "//mesop/components/{component_name}/e2e",',
  )

  # Update testing index.py file
  update_file(
    path=os.path.join(current_dir(), "..", "mesop", "testing", "index.py"),
    target="# REF(//scripts/gen_component.py):insert_component_e2e_import_export",
    content=f"import mesop.components.{component_name}.e2e as {component_name}_e2e",
    before=True,
  )

  update_component_renderer()

  update_dev_tools_deserializer()

  # Update dev_tools/service/BUILD
  update_file(
    path=os.path.join(
      web_src_dir(),
      "dev_tools",
      "services",
      "BUILD",
    ),
    target="# REF(//scripts/gen_component.py):insert_component_jspb_proto_import",
    content=f'    "//mesop/components/{component_name}:{component_name}_jspb_proto",',
  )

  print("Finished generating new component: " + component_name)


def update_component_renderer():
  component_renderer_path = os.path.join(web_src_dir(), "component_renderer")

  update_file(
    path=os.path.join(
      component_renderer_path,
      "component_renderer.ng.html",
    ),
    target="<!-- REF(//scripts/gen_component.py):insert_component -->",
    content="""<ng-container *ngIf="type()?.getName() == '[component_name]'">
  @defer (on viewport) {
  <mesop-[kebab-case] [key]="key()" [type]="type()!" />
  } @placeholder {
  <component-loader />
  }
</ng-container>
""".replace("[CamelCase]", camel_case())
    .replace("[kebab-case]", kebab_case())
    .replace("[component_name]", component_name),
    before=True,
  )

  update_file(
    path=os.path.join(component_renderer_path, "BUILD"),
    target="# REF(//scripts/gen_component.py):insert_component_import",
    content=f'    "//mesop/components/{component_name}:ng",',
  )

  ts_path = os.path.join(component_renderer_path, "component_renderer.ts")
  update_file(
    path=ts_path,
    target="// REF(//scripts/gen_component.py):insert_ts_import",
    content=f'import {{ {camel_case()}Component }} from "../../../mesop/components/{component_name}/{component_name}";',
  )
  update_file(
    path=ts_path,
    target="// REF(//scripts/gen_component.py):insert_ng_import",
    content=f"    {camel_case()}Component,",
  )


def update_dev_tools_deserializer():
  deserializer_path = os.path.join(
    web_src_dir(),
    "dev_tools",
    "services",
    "type_deserializer.ts",
  )
  type = "{" + f"{camel_case()}Type" + "}"
  update_file(
    path=deserializer_path,
    target="// REF(//scripts/gen_component.py):insert_component_jspb_proto_import",
    content=f'import {type} from "mesop/mesop/components/{component_name}/{component_name}_jspb_proto_pb/mesop/components/{component_name}/{component_name}_pb";',
  )
  update_file(
    path=deserializer_path,
    target="// REF(//scripts/gen_component.py):insert_register_deserializer",
    content=f"""this.registerDeserializer("{component_name}", (value) =>
      {camel_case()}Type.deserializeBinary(value).toObject(),
    );
    """,
  )


##################
# UTILITIES
##################


def update_file(path: str, target: str, content: str, before: bool = False):
  with open(path) as f:
    lines = f.readlines()

  for i in range(len(lines)):
    if target in lines[i]:
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
