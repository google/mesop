load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "THIRD_PARTY_PY_FLASK", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "server",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/component_helpers",
        "//mesop/editor",
        "//mesop/events",
        "//mesop/protos:ui_py_pb2",
        "//mesop/utils",
        "//mesop/warn",
    ] + THIRD_PARTY_PY_ABSL_PY + THIRD_PARTY_PY_FLASK,
    # Note: prod_server.py has a runtime dependency on
    # //mesop/web/src/app/prod:web_package, so you must include it
    # in the consuming py_binary's data attribute.
)

py_test(
    name = "wsgi_app_test",
    srcs = ["wsgi_app_test.py"],
    deps = [":server"] + THIRD_PARTY_PY_PYTEST,
)

py_test(
    name = "static_file_serving_test",
    srcs = ["static_file_serving_test.py"],
    deps = [":server"] + THIRD_PARTY_PY_PYTEST,
)
