load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "dev_tools",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":dev_tools.css"],
    deps = [
        "//optic/protos:ui_jspb_proto",
        "//web/src/dev_tools/components_panel",
        "//web/src/dev_tools/logs_panel",
    ] + ANGULAR_CORE_DEPS,
)

sass_binary(
    name = "styles",
    src = "dev_tools.scss",
    sourcemap = False,
)
