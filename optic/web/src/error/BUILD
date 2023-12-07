load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "error",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":error_box.css"],
    deps = [
        "//optic/protos:ui_jspb_proto",
        "//optic/web/src/component_renderer",
        "//optic/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

sass_binary(
    name = "styles",
    src = "error_box.scss",
    sourcemap = False,
)
