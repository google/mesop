load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module", "ng_test_library", "ng_web_test_suite", "sass_binary")

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
        "//mesop/web/src/dev_tools/components_panel",
        "//mesop/web/src/dev_tools/logs_panel",
        "//mesop/web/src/dev_tools/services",
    ] + ANGULAR_CORE_DEPS,
)

ng_test_library(
    name = "dev_tools_tests_lib",
    srcs = glob(["*_spec.ts"]),
    deps = [":dev_tools"],
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
