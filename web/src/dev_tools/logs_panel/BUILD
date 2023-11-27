load("//tools:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "logs_panel",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]) + [":logs_panel.css"],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/component_renderer",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "logs_panel.scss",
    sourcemap = False,
)
