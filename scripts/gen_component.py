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

    print("Start generating new component: " + component_name)
    copy_template(component_name)
    update_e2e_init(component_name)
    rename_and_update_files(component_name)
    update_component_build(component_name)
    update_py_export(component_name)
    update_py_build(component_name)
    update_testing_build(component_name)
    update_testing_index_py(component_name)
    update_component_renderer(component_name)
    print("Finished generating new component: " + component_name)


def update_component_renderer(component_name: str):
    component_renderer_path = os.path.join(
        get_current_directory(), "..", "web", "src", "component_renderer"
    )

    with open(component_renderer_path + "/component_renderer.ng.html", "r") as f:
        lines = f.readlines()

    template_call = (
        """<ng-container *ngIf="type()?.getName() == '[component_name]'">
  @defer (on viewport) {
  <optic-[kebab-case] [key]="key()" [type]="type()!" />
  } @placeholder {
  <component-loader />
  }
</ng-container>
""".replace("[CamelCase]", camel_case(component_name))
        .replace("[kebab-case]", kebab_case(component_name))
        .replace("[component_name]", component_name)
    )

    for i in range(len(lines)):
        if "<!-- REF(//scripts/gen_component.py):insert_component -->" in lines[i]:
            lines.insert(i, template_call + "\n")
            break

    with open(component_renderer_path + "/component_renderer.ng.html", "w") as f:
        f.writelines(lines)

    # Update BUILD
    build_path = os.path.join(component_renderer_path, "BUILD")

    with open(build_path, "r") as f:
        lines = f.readlines()

    import_line = f'    "//optic/components/{component_name}:ng",'

    for i in range(len(lines)):
        if "# REF(//scripts/gen_component.py):insert_component_import" in lines[i]:
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
        if "// REF(//scripts/gen_component.py):insert_ts_import" in lines[i]:
            lines.insert(i + 1, ts_import_line + "\n")
            break

    for i in range(len(lines)):
        if "// REF(//scripts/gen_component.py):insert_ng_import" in lines[i]:
            lines.insert(i + 1, ng_import_line + "\n")
            break

    with open(component_renderer_ts_path, "w") as f:
        f.writelines(lines)


def update_py_build(component_name: str):
    build_path = os.path.join(get_current_directory(), "..", "optic", "BUILD")

    with open(build_path, "r") as f:
        lines = f.readlines()

    import_line = f'    "//optic/components/{component_name}:py",'

    for i in range(len(lines)):
        if "# REF(//scripts/gen_component.py):insert_component_import" in lines[i]:
            lines.insert(i + 1, import_line + "\n")
            break

    with open(build_path, "w") as f:
        f.writelines(lines)


def update_py_export(component_name: str):
    init_path = os.path.join(get_current_directory(), "..", "optic", "__init__.py")

    with open(init_path, "r") as f:
        lines = f.readlines()

    import_line = f"from optic.components.{component_name}.{component_name} import {component_name} as {component_name}"

    for i in range(len(lines)):
        if (
            "# REF(//scripts/gen_component.py):insert_component_import_export"
            in lines[i]
        ):
            lines.insert(i, import_line + "\n")
            break

    with open(init_path, "w") as f:
        f.writelines(lines)


def update_testing_index_py(component_name: str):
    index_path = os.path.join(
        get_current_directory(), "..", "optic", "testing", "index.py"
    )

    with open(index_path, "r") as f:
        lines = f.readlines()

    import_line = (
        f"import optic.components.{component_name}.e2e as {component_name}_e2e"
    )

    for i in range(len(lines)):
        if (
            "# REF(//scripts/gen_component.py):insert_component_e2e_import_export"
            in lines[i]
        ):
            lines.insert(i, import_line + "\n")
            break

    with open(index_path, "w") as f:
        f.writelines(lines)


def update_testing_build(component_name: str):
    build_path = os.path.join(
        get_current_directory(), "..", "optic", "testing", "BUILD"
    )

    with open(build_path, "r") as f:
        lines = f.readlines()

    import_line = f'    "//optic/components/{component_name}/e2e",'

    for i in range(len(lines)):
        if "# REF(//scripts/gen_component.py):insert_component_e2e_import" in lines[i]:
            lines.insert(i + 1, import_line + "\n")
            break

    with open(build_path, "w") as f:
        f.writelines(lines)


def camel_case(component_name: str):
    """
    Split underscore and make it UpperCamelCase
    """
    return "".join(x.title() for x in component_name.split("_"))


def kebab_case(component_name: str):
    """
    Split underscore and make it kebab-case
    """
    return "-".join(x for x in component_name.split("_"))


def update_component_build(component_name: str):
    dst_dir = get_dst_dir(component_name)
    replace_component_name_ref(
        path=os.path.join(dst_dir, "BUILD"), component_name=component_name
    )


def rename_and_update_files(component_name: str):
    replace_component_name_ref(
        path=rename_file(component_name, ".py"), component_name=component_name
    )
    replace_component_name_ref(
        path=rename_file(component_name, ".ts"), component_name=component_name
    )
    rename_file(component_name, ".ng.html")
    proto_path = rename_file(component_name, ".proto")
    replace_component_name_ref(path=proto_path, component_name=component_name)

    new_app_py_path = rename_file(
        component_name, ".py", filename_suffix="_app", dir="e2e"
    )
    replace_component_name_ref(path=new_app_py_path, component_name=component_name)
    new_test_ts_path = rename_file(
        component_name, ".ts", filename_suffix="_test", dir="e2e"
    )
    replace_component_name_ref(path=new_test_ts_path, component_name=component_name)


def update_e2e_init(component_name: str):
    replace_component_name_ref(
        path=os.path.join(get_dst_dir(component_name), "e2e", "__init__.py"),
        component_name=component_name,
    )


def replace_component_name_ref(path: str, component_name: str):
    with open(path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = (
            lines[i]
            .replace("{component_name}", component_name)
            .replace("{component-name}", kebab_case(component_name))
            .replace("ComponentName", camel_case(component_name))
            .replace("component_name", component_name)
        )

    with open(path, "w") as f:
        f.writelines(lines)


def rename_file(
    component_name: str, extension: str, filename_suffix: str = "", dir: str = ""
) -> str:
    dst_dir = get_dst_dir(component_name)
    old_file_path = os.path.join(
        dst_dir, dir, "component_name" + filename_suffix + extension
    )
    new_file_path = os.path.join(
        dst_dir, dir, component_name + filename_suffix + extension
    )

    os.rename(old_file_path, new_file_path)
    return new_file_path


def copy_template(component_name: str):
    """
    Copies the directory in component_template and puts it in //optic/components/<component_name>"""

    src_dir = os.path.join(get_current_directory(), "component_template")
    dst_dir = get_dst_dir(component_name)

    shutil.copytree(src_dir, dst_dir)


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def get_dst_dir(component_name: str):
    return os.path.join(
        get_current_directory(), "..", "optic", "components", component_name
    )


if __name__ == "__main__":
    main()
