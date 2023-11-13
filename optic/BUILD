load("//builddefs:defs.bzl", "py_binary", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@my_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//:optic_internal"],
)

py_library(
    name = "optic",
    srcs = ["__init__.py"],
    deps = [
        "//optic/components",
        "//optic/state",
    ],
)

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        ":optic",
        "//optic/examples",
    ],
    main = "cli.py",
    deps = [
        requirement("absl-py"),
        "//optic/lib",
        "//optic/server:dev_server",
    ],
)

compile_pip_requirements(
    name = "pip_requirements",
    requirements_in = ":requirements.txt",
    requirements_txt = ":requirements_lock.txt",
)
