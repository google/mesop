"""
Run from the root of the repo:
python scripts/gen_component.py $component_name
"""
import shutil
import os

import argparse


def main():
    parser = argparse.ArgumentParser(description="Process a single CLI argument.")
    parser.add_argument("component_name", type=str, help="The CLI argument to process")

    args = parser.parse_args()

    component_name = args.component_name

    print("Generating new component: " + component_name)
    copy_template(component_name)
    rename_files(component_name)
    update_ts(component_name)
    update_py(component_name)
    update_py_export(component_name)
    update_py_build(component_name)
    update_component_renderer(component_name)


def update_component_renderer(component_name):
    """
    Open file web/src/component_renderer/component_renderer.html and before the line "<!-- INSERT NEW COMPONENT HERE -->" insert the block"baz"
    """
    component_renderer_path = os.path.join(
        get_current_directory(), "..", "web", "src", "component_renderer"
    )

    with open(component_renderer_path + "/component_renderer.html", "r") as f:
        lines = f.readlines()

    template_call = """<ng-container *ngIf="data()?.get[CamelCase]() != null">
  @defer (on viewport) {
  <app-[kebab-case] [config]="data()!.get[CamelCase]()!" />
  } @placeholder {
  <component-loader />
  }
</ng-container>
""".replace("[CamelCase]", camel_case(component_name)).replace(
        "[kebab-case]", kebab_case(component_name)
    )

    for i in range(len(lines)):
        if "<!-- INSERT NEW COMPONENT HERE -->" in lines[i]:
            lines.insert(i, template_call + "\n")
            break

    with open(component_renderer_path + "/component_renderer.html", "w") as f:
        f.writelines(lines)

    # Update BUILD
    build_path = os.path.join(component_renderer_path, "BUILD")

    with open(build_path, "r") as f:
        lines = f.readlines()

    import_line = f'    "//optic/components/{component_name}:ng",'

    for i in range(len(lines)):
        if "# INSERT COMPONENT IMPORTS HERE:" in lines[i]:
            lines.insert(i + 1, import_line + "\n")
            break

    with open(build_path, "w") as f:
        f.writelines(lines)

    # Update component_renderer.ts
    component_renderer_ts_path = os.path.join(
        component_renderer_path, "component_renderer.ts"
    )

    with open(component_renderer_ts_path, "r") as f:
        lines = f.readlines()

    ts_import_line = f'import {{ {camel_case(component_name)}Component }} from "../../../optic/components/{component_name}/{component_name}";'
    ng_import_line = f"    {camel_case(component_name)}Component,"
    for i in range(len(lines)):
        if "// INSERT COMPONENT TS IMPORTS HERE:" in lines[i]:
            lines.insert(i + 1, ts_import_line + "\n")
            break

    for i in range(len(lines)):
        if "// INSERT COMPONENT NG IMPORTS HERE:" in lines[i]:
            lines.insert(i + 1, ng_import_line + "\n")
            break

    with open(component_renderer_ts_path, "w") as f:
        f.writelines(lines)


def update_py_build(component_name):
    build_path = os.path.join(get_current_directory(), "..", "optic", "BUILD")

    with open(build_path, "r") as f:
        lines = f.readlines()

    import_line = f'    "//optic/components/{component_name}:py",'

    for i in range(len(lines)):
        if "# INSERT COMPONENT IMPORT HERE:" in lines[i]:
            lines.insert(i + 1, import_line + "\n")
            break

    with open(build_path, "w") as f:
        f.writelines(lines)


def update_py_export(component_name):
    """
    Reads the optic/__init__.py file and adds an export statement for the new component
    """

    init_path = os.path.join(get_current_directory(), "..", "optic", "__init__.py")

    with open(init_path, "r") as f:
        lines = f.readlines()

    import_line = f"from optic.components.{component_name}.{component_name} import {component_name} as {component_name}"

    for i in range(len(lines)):
        if "### COMPONENTS: END ###" in lines[i]:
            lines.insert(i, import_line + "\n")
            break

    with open(init_path, "w") as f:
        f.writelines(lines)


def update_ts(component_name):
    dst_dir = get_dst_dir(component_name)
    ts_file_path = dst_dir + "/" + component_name + ".ts"

    with open(ts_file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = (
            lines[i]
            .replace("{component_name}", component_name)
            .replace("{component-name}", kebab_case(component_name))
            .replace("ComponentName", camel_case(component_name))
        )

    with open(ts_file_path, "w") as f:
        f.writelines(lines)


def update_py(component_name):
    dst_dir = get_dst_dir(component_name)
    ts_file_path = dst_dir + "/" + component_name + ".py"

    with open(ts_file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace("component_name", component_name)

    with open(ts_file_path, "w") as f:
        f.writelines(lines)


def camel_case(component_name):
    """
    Split underscore and make it UpperCamelCase
    """
    return "".join(x.title() for x in component_name.split("_"))


def kebab_case(component_name):
    """
    Split underscore and make it kebab-case
    """
    return "-".join(x for x in component_name.split("_"))


def rename_files(component_name):
    rename_file(component_name, ".py")
    rename_file(component_name, ".ts")
    rename_file(component_name, ".html")


def rename_file(component_name, extension):
    dst_dir = get_dst_dir(component_name)
    old_file_path = dst_dir + "/button" + extension
    new_file_path = dst_dir + "/" + component_name + extension

    try:
        os.rename(old_file_path, new_file_path)
    except OSError as e:
        print(f"Error renaming: {e.strerror}")


def copy_template(component_name):
    """
    Copies the directory in component_template and puts it in //optic/components/<component_name>"""

    src_dir = os.path.join(get_current_directory(), "component_template")
    dst_dir = get_dst_dir(component_name)

    shutil.copytree(src_dir, dst_dir)


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def get_dst_dir(component_name):
    return os.path.join(
        get_current_directory(), "..", "optic", "components", component_name
    )


print(get_current_directory())

if __name__ == "__main__":
    main()
