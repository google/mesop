load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
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
        "//optic/protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS,
)

sass_binary(
    name = "styles",
    src = "component_tree.scss",
    sourcemap = False,
)
