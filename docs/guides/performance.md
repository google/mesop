# Performance

Occasionally, you may run into performance issues with your Mesop app. Here are some tips to help you improve your app's performance.

## Determine the root cause

The first step in debugging performance issues is to identify the cause of the issue. Follow the [Debugging with DevTools guide](./debugging.md#debugging-with-devtools) and use the Console and Network tab to identify the issue.

## Common performance bottlenecks and solutions

### Optimizing state size

If you notice with Chrome DevTools that you're sending very large network payloads between client and server, it's likely that your state is too large.

Because the state object is serialized and sent back and forth between the client and server, you should try to keep the state object reasonably sized. For example, if you store a very large string (e.g. base64-encoded image) in state, then it will degrade performance of your Mesop app.

The following are recommendations to help you avoid large state payloads:

#### Store state in memory

Mesop has a feature that allows you to store state in memory rather than passing the
full state on every request. This may help improve performance when dealing with large
state objects. The caveat is that, storing state in memory contains its own set of
problems that you must carefully consider. See the [config section](../api/config.md#mesop_state_session_backend)
for details on how to use this feature.

If you are running Mesop on a single replica or you can enable [session affinity](https://cloud.google.com/run/docs/configuring/session-affinity), then this is a good option.

#### Store state externally

You can also store state outside of Mesop using a database or a storage service. This is a good option if you have a large amount of state data. For example, rather than storing images in the state, you can store them in a bucket service like [Google Cloud Storage](https://cloud.google.com/storage) and send [signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls) to the client so that it can directly fetch the images without going through the Mesop server.

### Handling high user load

If you notice that your Mesop app is running slowly when you have many concurrent users, you can try to scale your Mesop app.

#### Increase the number of replicas

To handle more concurrent users, you can scale your Mesop app horizontally by increasing the number of replicas (instances) running your application. This can be achieved through various cloud services that offer autoscaling features:

1. Use a managed service like Google Cloud Run, which automatically scales your app based on traffic. Follow Mesop's [Cloud Run deployment guide](./deployment.md#deploying-to-cloud-run) for details.

2. Manually adjust the number of replicas to a higher number.

3. Tune gunicorn settings. If you're using [gunicorn](https://docs.gunicorn.org/) to serve your Mesop app, you can adjust gunicorn settings to [increase the number of workers](https://docs.gunicorn.org/en/latest/design.html#how-many-workers). This can help to increase the number of concurrent users your Mesop app can handle.

Whichever platform you choose, make sure to configure the replica settings to match your app's performance requirements and budget constraints.
