load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//protos:ui_jspb_proto",
        "//web/src/dev_tools/services",
    ] + ANGULAR_CORE_DEPS,
)
