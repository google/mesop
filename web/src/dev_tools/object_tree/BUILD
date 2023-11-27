load("//tools:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "object_tree",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":object_tree.css"],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/component_renderer",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "object_tree.scss",
    sourcemap = False,
)
