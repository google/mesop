load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "ng_test_library", "ng_web_test_suite", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "dev_tools",
    srcs = glob(
        [
            "*.ts",
        ],
        exclude = ["*_spec.ts"],
    ),
    assets = glob([
        "*.ng.html",
    ]) + [":dev_tools.css"],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/dev_tools/editor_panel",
        "//mesop/web/src/dev_tools/logs_panel",
        "//mesop/web/src/dev_tools/services",
        "//mesop/web/src/services",
        "//mesop/web/src/utils",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

ng_test_library(
    name = "dev_tools_tests_lib",
    srcs = glob(["*_spec.ts"]),
    deps = [
        ":dev_tools",
        "//mesop/web/src/editor",
        "//mesop/web/src/services",
    ],
)

ng_web_test_suite(
    name = "unit_tests",
    deps = [
        ":dev_tools_tests_lib",
    ],
)

sass_binary(
    name = "styles",
    src = "dev_tools.scss",
    sourcemap = False,
)
