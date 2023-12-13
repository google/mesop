load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/dev_tools/services",
    ] + ANGULAR_CORE_DEPS,
)
