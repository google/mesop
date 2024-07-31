load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module", "ng_test_library", "ng_web_test_suite", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "component_renderer",
    srcs = glob(
        [
            "*.ts",
        ],
        exclude = ["*_spec.ts"],
    ),
    assets = glob([
        "*.ng.html",
    ]) + ["component_renderer.css"],
    deps = [
        # REF(//scripts/scaffold_component.py):insert_component_import
        "//mesop/components/autocomplete:ng",
        "//mesop/components/link:ng",
        "//mesop/components/html:ng",
        "//mesop/components/uploader:ng",
        "//mesop/components/embed:ng",
        "//mesop/components/table:ng",
        "//mesop/components/sidenav:ng",
        "//mesop/components/video:ng",
        "//mesop/components/audio:ng",
        "//mesop/components/image:ng",
        "//mesop/components/slider:ng",
        "//mesop/components/select:ng",
        "//mesop/components/radio:ng",
        "//mesop/components/slide_toggle:ng",
        "//mesop/components/progress_spinner:ng",
        "//mesop/components/progress_bar:ng",
        "//mesop/components/icon:ng",
        "//mesop/components/divider:ng",
        "//mesop/components/badge:ng",
        "//mesop/components/tooltip:ng",
        "//mesop/components/input:ng",
        "//mesop/components/markdown:ng",
        "//mesop/components/box:ng",
        "//mesop/components/box:box_jspb_proto",
        "//mesop/components/button:ng",
        "//mesop/components/checkbox:ng",
        "//mesop/components/text:ng",
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/utils",
    ] + ANGULAR_CDK_TS_DEPS + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

sass_binary(
    name = "component_renderer_styles",
    src = "component_renderer.scss",
    sourcemap = False,
)

ng_test_library(
    name = "tests_lib",
    srcs = glob(["*_spec.ts"]),
    deps = [
        ":component_renderer",
    ],
)

ng_web_test_suite(
    name = "unit_tests",
    deps = [
        ":tests_lib",
    ],
)
