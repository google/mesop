lsof -t -i:32123 | xargs kill && \
ibazel run //mesop/cli:dev_cli -- --path="mesop/mesop/index.py"
