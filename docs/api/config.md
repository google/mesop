# Config

## Overview

Mesop is configured at the application level using environment variables.

## Configuration values

Mesop currently only has one configuration value, but more will be added in the future.

### MESOP_STATE_SESSION_BACKEND

Sets the backend to use for caching state data server-side. This makes it so state does
not have to be sent to the server on every request, reducing bandwidth, especially if
you have large state objects.

The only backend option available at the moment is `memory`.

Users should be careful when using the `memory` backend. Each Mesop process has their
own RAM, which means cache misses will be common if there is no session affinity. In
addition, the amount of RAM must be carefully specified per machine in accordance with
the expected user traffic and state size.

The safest option for using the `memory` backend is to use a single a process with a
good amount of RAM. Python is not the most memory efficient, especially data structures
such as dicts.

The drawback of being limited to a single process is that requests will take longer to
process since only one request can be handled at a time. This is especially problematic
if your application contains long running API calls.

If session affinity is available, you can scale up multiple machines, each running
single processes.

**Default:** `none`

## Usage Examples

### One-liner

You can specify the environment variables before the mesop command.

```sh
MESOP_STATE_SESSION_BACKEND=memory mesop main.py
```

### Use a .env file

Mesop also supports `.env` files. This is nice since you don't have to keep setting
the environment variables. In addition, the variables are only set when the application
is run.

```sh title=".env"
MESOP_STATE_SESSION_BACKEND=memory
```

When you run your Mesop app, the .env file will then be read.

```sh
mesop main.py
```
