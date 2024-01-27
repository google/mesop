load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "THIRD_PARTY_PY_FLASK", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "server",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/editor",
        "//mesop/protos:ui_py_pb2",
        "//mesop/utils",
    ] + THIRD_PARTY_PY_ABSL_PY + THIRD_PARTY_PY_FLASK,
    # Note: prod_server.py has a runtime dependency on
    # //mesop/web/src/app/prod:web_package, so you must include it
    # in the consuming py_binary's data attribute.
)
