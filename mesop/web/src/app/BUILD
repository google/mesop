load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "esbuild_config", "ng_module", "sass_binary", "sass_external_binary", "sass_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "app",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "app.ng.html",
        "app_styles.css",
    ],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/component_renderer",
        "//mesop/web/src/dev_tools",
        "//mesop/web/src/dev_tools/services",
        "//mesop/web/src/error",
        "//mesop/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

sass_binary(
    name = "app_styles",
    src = "app_styles.scss",
    sourcemap = False,
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

sass_library(
    name = "normalize",
    srcs = [
        "_normalize.scss",
    ],
)

sass_external_binary(
    name = "styles",
    src = "styles.scss",
    external_deps = [
        "@npm//@angular/material",
    ],
    sourcemap = False,
    deps = [
        ":normalize",
    ],
)
