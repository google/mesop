load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "command_dialog",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":command_dialog.css"],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/dev_tools/services",
        "//mesop/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

sass_binary(
    name = "styles",
    src = "command_dialog.scss",
    sourcemap = False,
)
