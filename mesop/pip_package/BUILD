package(
    default_visibility = ["//build_defs:mesop_internal"],
)

licenses(["notice"])

sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = [
        "LICENSE",
        "MANIFEST.in",
        "README.md",
        "requirements.txt",
        "setup.cfg",
        "setup.py",
        ":deterministic_tar_gz",
        "//mesop",  # Main Mesop target
        "//mesop:version.py",
        "//mesop/bin",  # CLI binary
        "//mesop/labs",  # Mesop labs target
    ],
)

py_binary(
    name = "deterministic_tar_gz",
    srcs = ["deterministic_tar_gz.py"],
)
