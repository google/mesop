load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "button",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "button.html",
    ],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/services",
        "@npm//@angular/compiler",
        "@npm//@angular/material",
    ],
)
