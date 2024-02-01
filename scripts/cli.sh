(lsof -t -i:32123 | xargs kill) || true && \
ibazel run //mesop/cli -- --path="mesop/mesop/example_index.py"
