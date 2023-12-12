lsof -t -i:8080 | xargs kill && \
ibazel run //optic/cli -- --path="optic/optic/testing/index.py"
