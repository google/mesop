load("//build_defs:defaults.bzl", "ng_test_library", "ng_web_test_suite", "ts_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ts_library(
    name = "utils",
    srcs = glob(
        ["*.ts"],
        exclude = ["*_spec.ts"],
    ),
    deps = ["//mesop/protos:ui_jspb_proto"],
)

ng_test_library(
    name = "utils_test_lib",
    srcs = glob(["*_spec.ts"]),
    deps = [
        ":utils",
        "//mesop/protos:ui_jspb_proto",
    ],
)

ng_web_test_suite(
    name = "unit_tests",
    deps = [
        ":utils_test_lib",
    ],
)
