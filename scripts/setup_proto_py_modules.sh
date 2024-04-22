# Needed for VS Code to provide Python type-checking against generated proto stubs.
bazel_bin_path=$(bazel info bazel-bin)

touch "${bazel_bin_path}/mesop/__init__.py" && \
touch "${bazel_bin_path}/mesop/protos/__init__.py" && \
touch "${bazel_bin_path}/mesop/components/__init__.py" && \
find "${bazel_bin_path}/mesop/components/" -type d -exec touch {}/__init__.py \; && \
# Purposefully have generator at the end since it's not always built and might error out
# which isn't a big deal because VS Code can still type-check the rest of the codebase.
touch "${bazel_bin_path}/generator/__init__.py";
