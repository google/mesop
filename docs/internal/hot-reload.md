# Hot Reload

One of Mesop's key benefits is that it provides a fast iteration cycle through hot reload. This means whenever a Mesop developer changes their Mesop app code, their browser window will automaticall reload and execute the new app code while preserving the existing state. This isn't guaranteed to work, for example, if the State class is modified in an incompatible way, but it should work for >90% of the build-edit loops (e.g. tweaking the UI, calling new components).

## How it works

See: [https://github.com/google/mesop/pull/211](https://github.com/google/mesop/pull/211)

## Design decisions

### What to reload

Right now we reload all the modules loaded by the Mesop application. However, this results in a lot of unnecessary modules being reloaded and can be quite slow if there's a heavy set of transitive dependencies.

Instead, I'm thinking we can use a heuristic where we calculate the existing package based on the file path passed in and *only* reload modules which are in the current package or a sub-package. Effectively this is only reloading modules within the target file's subtree.

This seems like a pretty reasonable heuristic where it reloads all the application modules without reloading the entire dependency graph. Previously I tried reloading *only* the module passed in via `--path`, however this was too limiting as it meant shared code (e.g. a navmenu) would not get hot-reloaded.

### When to reload

With the previous design decision, re-executing a module should be much faster, but we still need to guard against the case where the live reload occurs too quickly in the client side. Options:

- **Wait a fixed timeout** - A simple heuristic could just be to wait 500ms since in theory, all the application code (with the non-application dependnecies cached) should re-execute fairly quickly.
- **Client retry/reload** - Another approach could be to retry a client-side reload N times (e.g. 3) if we get an error. The pattern could be: 1. save state to local storage, 2. trigger reload, 3. if reload results in a successful render, we clear the state _OR_ if reload results in an error, we trigger a reload (and persist in local storage which retry attempt this is).
- **Server loop** - In the common error case where the server is still re-executing the module and the client reloads, it will hit path not found because the path hasn't been registered yet. One way of mitigating this is to simply do a sleep in debug mode. We can even do an exponential backoff for the sleep (e.g. wait 300ms, 900ms, 2700ms).
- **Preferred appproach** - given the trade-offs, I think **Server loop** is the best option as it's relatively simple to implement, robust and doesn't incur a significant delay in the happy case.

### Abstracting ibazel-specific details

Since Google's internal equivalent of ibazel doesn't work exactly the same, we should treat HotReloadService as an abstract base class and then extend it for Ibazel (and the internal variant).
