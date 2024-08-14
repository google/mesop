# Performance

Occasionally, you may run into performance issues with your Mesop app. Here are some tips to help you improve your app's performance.

## Determine the root cause

The first step in debugging performance issues is to identify the cause of the issue. Follow the [Debugging with DevTools guide](./debugging.md#debugging-with-devtools) and use the Console and Network tab to identify the issue.

## Common issues

### State is too large

If you notice with Chrome DevTools that you're sending very large network payloads between client and server, it's likely that your state is too large.

Because the state class is serialized and sent back and forth between the client and server, you should try to keep the state class reasonably sized. For example, if you store a very large string (e.g. base64-encoded image) in state, then it will degrade performance of your Mesop app.

The following are recommendations to help you avoid large state payloads:

#### Store state in memory

Mesop has a feature that allows you to store state in memory rather than passing the
full state on every request. This may help improve performance when dealing with large
state objects. The caveat is that storing state in memory contains its own set of
problems that you must carefully consider. See the [config section](../api/config.md#mesop_state_session_backend)
for details on how to use this feature.

If you are running Mesop on a single replica or you can enable [session affinity](https://cloud.google.com/run/docs/configuring/session-affinity), then this is a good option.

#### Store state externally

You can also store state outside of Mesop using a database or a storage service. This is a good option if you have a large amount of state data. For example, rather than storing images in the state, you can store in them in a bucket service like [Google Cloud Storage](https://cloud.google.com/storage) and send [signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls) to the client so that it can directly fetch the images without going through the Mesop server.

### Too many users

If you notice that your Mesop app is running slowly when you have many concurrent users, you can try to scale your Mesop app.

#### Use Cloud Run

Cloud Run is a managed Google Cloud service that can scale your Mesop app to handle more concurrent users.
You can use the [autoscaling feature](https://cloud.google.com/run/docs/about-instance-autoscaling) to scale your Mesop app up and down based on the traffic to your app. Follow Mesop's [Cloud Run deployment guide](./deployment.md#deploying-to-cloud-run) to deploy your Mesop app to Cloud Run.

You can also use other Cloud services which provide autoscaling features.

#### Adjust your gunicorn settings

If you're using [gunicorn](https://docs.gunicorn.org/) to serve your Mesop app, you can adjust gunicorn settings to [increase the number of workers](https://docs.gunicorn.org/en/latest/design.html#how-many-workers). This can help to increase the number of concurrent users your Mesop app can handle.
