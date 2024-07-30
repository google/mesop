load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "THIRD_PARTY_JS_RXJS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "shell",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "shell.ng.html",
        "shell.css",
    ],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/component_renderer",
        "//mesop/web/src/error",
        "//mesop/web/src/services",
        "//mesop/web/src/utils",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS + THIRD_PARTY_JS_RXJS,
)

sass_binary(
    name = "shell_styles",
    src = "shell.scss",
    sourcemap = False,
)
