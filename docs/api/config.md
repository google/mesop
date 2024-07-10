# Config

## Overview

Mesop is configured at the application level using environment variables.

## Configuration values

### MESOP_STATE_SESSION_BACKEND

Sets the backend to use for caching state data server-side. This makes it so state does
not have to be sent to the server on every request, reducing bandwidth, especially if
you have large state objects.

The backend options available at the moment are `memory`, `file`, and `firestore`.

#### memory

Users should be careful when using the `memory` backend. Each Mesop process has their
own RAM, which means cache misses will be common if each server has multiple processes
and there is no session affinity. In addition, the amount of RAM must be carefully
specified per instance in accordance with the expected user traffic and state size.

The safest option for using the `memory` backend is to use a single process with a
good amount of RAM. Python is not the most memory efficient, especially when saving data
structures such as dicts.

The drawback of being limited to a single process is that requests will take longer to
process since only one request can be handled at a time. This is especially problematic
if your application contains long running API calls.

If session affinity is available, you can scale up multiple instances, each running
single processes.

#### file

Users should be careful when using the `file` backend. Each Mesop instance has their
own disk, which can be shared among multiple processes. This means cache misses will be
common if there are multiple instances and no session affinity.

If session affinity is available, you can scale up multiple instances, each running
multiple Mesop processes. If no session affinity is available, then you can only
vertically scale a single instance.

The bottleneck with this backend is the disk read/write performance. The amount of disk
space must also be carefully specified per instance in accordance with the expected user
traffic and state size.

You will also need to specify a directory to write the state data using
`MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR`.

#### GCP Firestore

This options uses [GCP Firestore](https://cloud.google.com/firestore?hl=en) to store
Mesop state sessions. The `(default)` database has a free tier that can be used for
for small demo applications with low traffic and moderate amounts of state data.

Since Firestore is decoupled from your Mesop server, it allows you to scale vertically
and horizontally without the considerations you'd need to make for the `memory` and
`file` backends.

In order to use Firestore, you will need a Google Cloud account with Firestore enabled.
Follow the instructions for [creating a Firestore in Native mode database](https://cloud.google.com/firestore/docs/create-database-server-client-library#create_a_in_native_mode_database).

Mesop is configured to use the `(default)` Firestore only. The GCP project is determined
using the Application Default Credentials (ADC) which is automatically configured for
you on GCP services, such as Cloud Run.

For local development, you can run this command:

```sh
gcloud auth application-default login
```

If you have multiple GCP projects, you may need to update the project associated
with the ADC:

```sh
GCP_PROJECT=gcp-project
gcloud config set project $GCP_PROJECT
gcloud auth application-default set-quota-project $GCP_PROJECT
```

Mesop leverages Firestore's [TTL policies](https://firebase.google.com/docs/firestore/ttl)
to delete stale state sessions. This needs to be set up using the following command,
otherwise old data will accumulate unnecessarily.

```sh
COLLECTION_NAME=collection_name
gcloud firestore fields ttls update expiresAt \
  --collection-group=$COLLECTION_NAME
```

By default, Mesop will use the collection name `mesop_state_sessions`, but this can be
overridden using `MESOP_STATE_SESSION_BACKEND_FIRESTORE_COLLECTION`.

**Default:** `none`

### MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR

This is only used when the `MESOP_STATE_SESSION_BACKEND` is set to `file`. This
parameter specifies where Mesop will read/write the session state. This means the
directory must be readable and writeable by the Mesop server processes.

### MESOP_STATE_SESSION_BACKEND_FIRESTORE_COLLECTION

This is only used when the `MESOP_STATE_SESSION_BACKEND` is set to `firestore`. This
parameter specifies which Firestore collection that Mesop will write state sessions to.

**Default:** `mesop_state_sessions`

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
MESOP_STATE_SESSION_BACKEND=file
MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR=/tmp/mesop-sessions
```

When you run your Mesop app, the .env file will then be read.

```sh
mesop main.py
```
