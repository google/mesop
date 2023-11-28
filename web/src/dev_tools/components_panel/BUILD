load("//tools:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "components_panel",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":components_panel.css"],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/dev_tools/component_tree",
        "//web/src/dev_tools/object_tree",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "components_panel.scss",
    sourcemap = False,
)
