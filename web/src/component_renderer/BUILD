load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "component_renderer",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        "//optic/components/button:ng",
        "//protos:ui_ts_proto",
        "//web/src/components/checkbox",
        "//web/src/components/text",
        "@npm//@angular/compiler",
    ],
)
