(lsof -t -i:32123 | xargs kill) || true && \
MESOP_WEB_COMPONENTS_HTTP_CACHE_KEY=$(git rev-parse HEAD) MESOP_HTTP_CACHE_JS_BUNDLE=true bazel run //mesop/cli -- --path=mesop/mesop/example_index.py --prod
