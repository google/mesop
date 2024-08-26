# Uses editor_cli which provides a faster development cycle than the regular "cli" target.
(lsof -t -i:32123 | xargs kill) || true && \
MESOP_EXPERIMENTAL_EDITOR_TOOLBAR=true \
ibazel run //mesop/cli:editor_cli -- --path="mesop/mesop/example_index.py" --reload_demo_modules
