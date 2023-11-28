lsof -t -i:8080 | xargs kill && \
ibazel run //optic/cli:dev_cli -- --path="optic/testing/index.py"
