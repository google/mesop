load("//build_defs:defaults.bzl", "PYTHON_RUNFILES_DEP", "THIRD_PARTY_PY_FLASK", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_library(
    name = "server",
    srcs = glob(["*.py"]),
    deps = [
        "//protos:ui_py_pb2",
    ] + PYTHON_RUNFILES_DEP + THIRD_PARTY_PY_FLASK,
    # Note: prod_server.py has a runtime dependency on
    # //web/src/app/prod:web_package, so you must include it
    # in the consuming py_binary's data attribute.
)
