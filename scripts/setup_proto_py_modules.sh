# Needed for VS Code to provide Python type-checking against generated proto stubs.
bazel_bin_path=$(bazel info bazel-bin)

touch "${bazel_bin_path}/optic/__init__.py" && \
touch "${bazel_bin_path}/optic/protos/__init__.py" && \
touch "${bazel_bin_path}/optic/components/__init__.py" &&
find "${bazel_bin_path}/optic/components/" -type d -exec touch {}/__init__.py \;
