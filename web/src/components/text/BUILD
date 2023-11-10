load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "text",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "text.html",
    ],
    deps = [
        "//protos:ui_ts_proto",
        "@npm//@angular/compiler",
    ],
)
