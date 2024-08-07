(lsof -t -i:32123 | xargs kill) || true && \
bazel run //mesop/cli -- --path=mesop/mesop/example_index.py --prod
