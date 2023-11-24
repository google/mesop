load("//builddefs:defs.bzl", "py_library")
load("@my_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//:optic_internal"],
)

py_library(
    name = "server",
    srcs = glob(["*.py"]),
    deps = [
        requirement("flask"),
        "//protos:ui_py_proto",
        "@rules_python//python/runfiles",
    ],
    # Note: prod_server.py has a runtime dependency on
    # //web/src/app/prod:web_package, so you must include it
    # in the consuming py_binary's data attribute.
)
