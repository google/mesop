# Description:
#  Tools for building the Mesop pip package.

load("@rules_python//python:py_binary.bzl", "py_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

licenses(["notice"])

genrule(
    name = "pip_package",
    # Pip packages are provided in a tarball because we can't statically
    # know the file names: they must contain the version,
    # which is only defined in a Python module. Dependents of this
    # target can extract the tarball and glob its contents.
    outs = ["pip_packages.tar.gz"],
    cmd = "$(execpath :build_pip_package) $@",
    tools = [
        ":build_pip_package",
    ],
)

sh_binary(
    name = "extract_pip_package",
    srcs = ["extract_pip_package.sh"],
    data = [":pip_package"],
)

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
        "//mesop/cli",  # CLI (which includes data dep on web app)
        "//mesop/labs",  # Mesop labs target
    ],
)

py_binary(
    name = "deterministic_tar_gz",
    srcs = ["deterministic_tar_gz.py"],
    srcs_version = "PY3",
)
