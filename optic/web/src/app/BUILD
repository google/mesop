load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "esbuild_config", "ng_module", "sass_external_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "app",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "app.ng.html",
    ],
    deps = [
        "//optic/protos:ui_jspb_proto",
        "//optic/web/src/component_renderer",
        "//optic/web/src/dev_tools",
        "//optic/web/src/dev_tools/services",
        "//optic/web/src/error",
        "//optic/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

sass_external_binary(
    name = "styles",
    src = "styles.scss",
    external_deps = [
        "@npm//@angular/material",
    ],
    sourcemap = False,
)
