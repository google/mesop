load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "ng",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/services",
        "@npm//@angular/compiler",
        "@npm//@angular/material",
    ],
)

py_library(
    name = "py",
    srcs = glob(["*.py"]),
    deps = [
        "//optic/component_helpers",
        "//protos:ui_py_proto",
    ],
)
