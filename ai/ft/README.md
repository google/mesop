# Fine-tuning & eval toolkit

This package contains tools for evaluating and creating a fine-tuning dataset.

## LLM lib

`llm_lib` contains the wrapper around interacting with the LLM and transforming the outputs. Ideally, we would reuse this across the offline (e.g. eval, fine-tuning) and online (e.g. visual editor) flows, but right now, I'm just copying and pasting it since it's quite experimental still.

## Generate

To generate outputs from an LLM:

```sh
python generate.py --model $model_name --run_name $run_name --num_inputs=5
```

> Note: look at `llm_lib.py` to see which model names you can pass in.

> Note: `num_inputs` is optional.

## Evaluate

**Prerequisites**:

- You must run the [sandbox](#sandbox).

To evaluate the generated outputs from the previous step:

```sh
python evaluate.py --model $model_name --run_name $run_name
```

This will do the following checks:

- Ensure the diff is patchable and generate the patched Python file
- Execute the patched Python file from top to bottom (note: this uses a regular Python interpreter and not the mesop CLI)
- Type-check the patched Python file

## Goldenizer

Goldenizer is similar to `evaluate.py` but runs it for the goldens dataset. Most of the code is shared through `eval_lib.py`.

## Viewer

**Prerequisites**:

- You must run the [sandbox](#sandbox) in order to run the Mesop appss.

To run the viewer:

```sh
mesop viewer.py
```

- To view a previous eval run, go to: localhost:32123/?model=$model&run=$run
- To view the goldens, go to: localhost:32123/?golden=true

## Sandbox

Start the sandbox:

```sh
cd sandbox
docker stop mesop-sandbox;
docker rm mesop-sandbox;
docker build -t mesop-sandbox . && docker run --name mesop-sandbox -d -p 8080:8080 mesop-sandbox;
```

## Dataset Formatter

Dataset formatter is a tool for formatting the dataset into a format that can be uploaded for fine-tuning.
