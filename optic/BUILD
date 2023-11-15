load("//builddefs:defs.bzl", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package(
    default_visibility = ["//:optic_internal"],
)

py_library(
    name = "optic",
    srcs = ["__init__.py"],
    deps = [
        "//optic/components",
        "//optic/state",
        "//optic/store",
    ],
)

compile_pip_requirements(
    name = "pip_requirements",
    requirements_in = ":requirements.txt",
    requirements_txt = ":requirements_lock.txt",
)
