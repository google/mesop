load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
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
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/external:marked",
        "//mesop/web/src/component_renderer",
        "//mesop/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

sass_binary(
    name = "styles",
    src = "error_box.scss",
    sourcemap = False,
)
