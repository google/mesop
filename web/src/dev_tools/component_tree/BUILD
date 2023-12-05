load("//build_defs:defaults.bzl", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "component_tree",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":component_tree.css"],
    deps = [
        "//protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

sass_binary(
    name = "styles",
    src = "component_tree.scss",
    sourcemap = False,
)
