lsof -t -i:32123 | xargs kill && \
ibazel run //mesop/cli -- --path="mesop/mesop/index.py"
