# Fine-tuning, synth generation & eval

```sh
python generate.py --model deepseek --run_name r2 --num_inputs=5
```

```sh
python evaluate.py --model deepseek --run_name r2
```

## Running the viewer

### Start sandbox in separate terminal

```sh
cd sandbox
docker stop mesop-sandbox;
docker rm mesop-sandbox;
docker build -t mesop-sandbox . && docker run --name mesop-sandbox -d -p 8080:8080 mesop-sandbox;
```

## Notes
