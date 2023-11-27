load("//tools:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "dev_tools",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":dev_tools.css"],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/dev_tools/logs_panel",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "dev_tools.scss",
    sourcemap = False,
)
