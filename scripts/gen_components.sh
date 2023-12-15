# Generate components
bazel run //generator:spec_generator -- --workspace_root=$(pwd) && \
bazel run //generator:component_generator
