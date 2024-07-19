mkdir -p gen/prompt_context && \
python dump_api_docs.py && \
python dump_github_discussions.py && \
python prompt.py > gen/prompt_context/prompt.txt
