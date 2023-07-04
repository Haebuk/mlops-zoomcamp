```bash
docker build -t stream-model-duration:v2 .
```

```bash
docker run -it --rm \
	-p 8080:8080 \
	-e AWS_DEFAULT_PROFILE=my-kade \
	-e PREDICTIONS_STREAM_NAME="ride_predictions" \
	-e RUN_ID="abf2e9dc119f4aa5baeffcce17ec7a83" \
	-e TEST_RUN="True" \
	stream-model-duration:v2
```