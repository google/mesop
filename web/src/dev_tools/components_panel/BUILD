load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
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
        "//protos:ui_jspb_proto",
        "//web/src/dev_tools/component_tree",
        "//web/src/dev_tools/object_tree",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS,
)

sass_binary(
    name = "styles",
    src = "components_panel.scss",
    sourcemap = False,
)
