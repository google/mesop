load("//build_defs:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "logs_panel",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":logs_panel.css"],
    deps = [
        "//protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/dev_tools/object_tree",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "logs_panel.scss",
    sourcemap = False,
)
