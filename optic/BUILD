load("//builddefs:defs.bzl", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package(
    default_visibility = ["//:optic_internal"],
)

py_library(
    name = "optic",
    srcs = ["__init__.py"],
    deps = [
        # REF(//scripts/gen_component.py):insert_component_import
        "//optic/components",
        "//optic/components/button:py",
        "//optic/components/checkbox:py",
        "//optic/components/text:py",
        "//optic/features",
        "//optic/state",
        "//optic/store",
    ],
)

compile_pip_requirements(
    name = "pip_requirements",
    requirements_in = ":requirements.txt",
    requirements_txt = ":requirements_lock.txt",
)
