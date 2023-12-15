# Needed for VS Code to provide Python type-checking against generated proto stubs.
bazel_bin_path=$(bazel info bazel-bin)

touch "${bazel_bin_path}/mesop/__init__.py" && \
touch "${bazel_bin_path}/component_specs/__init__.py" && \
touch "${bazel_bin_path}/mesop/protos/__init__.py" && \
touch "${bazel_bin_path}/mesop/components/__init__.py" &&
find "${bazel_bin_path}/mesop/components/" -type d -exec touch {}/__init__.py \;
