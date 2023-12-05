load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
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
        "//protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS,
)

sass_binary(
    name = "styles",
    src = "error_box.scss",
    sourcemap = False,
)
