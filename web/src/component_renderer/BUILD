load("//tools:defaults.bzl", "ng_module")

package(default_visibility = ["//visibility:public"])

ng_module(
    name = "component_renderer",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/components/text",
        "@npm//@angular/compiler",
    ],
)
