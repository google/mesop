lsof -t -i:8080 | xargs kill && \
bazel run //optic/cli -- --path="optic/testing/index.py"
