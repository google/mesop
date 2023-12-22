lsof -t -i:8080 | xargs kill && \
ibazel run //mesop/cli -- --path="mesop/mesop/examples/index.py"
