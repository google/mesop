load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
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
        "//optic/protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS + ANGULAR_CDK_TS_DEPS,
)

sass_binary(
    name = "styles",
    src = "object_tree.scss",
    sourcemap = False,
)
