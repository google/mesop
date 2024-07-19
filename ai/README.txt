# AI

This contains experimental code to support upcoming Mesop AI features.

All the scripts should be run in this directory (i.e. `cd ai`).

## How to use

### 1. Generate system prompt

First you'll need to generate the system prompt which is used to teach an LLM in-context about Mesop.

```sh
./gen_prompt.sh
```

### 2. Run eval

Next, you will want to run the eval script which generates LLM outputs (Gemini).
Be mindful about how many evals you're running as you will be billed for the usage.

```sh
python run_eval.py
```

### 3. Analyze the eval

Finally, you can look at the generated outputs inside `gen/eval/${EVAL_ROUND_NAME}` either directly or by using `eval_app.py`.

```sh
mesop eval_app.py
```

## Notes

- Ideally, we can have the LLM cite specific pages in its response, but this isn't working too well yet.
    - Need to fix heuristics of how URLs are printed out in prompt context generation.
    - Need to improve system instructions.
