# Debugging

VS Code is recomended for debugging your Mesop app, but you should be able to debug Mesop in other IDEs.

## Debugging in VS Code

**Pre-requisite:** ensure VS Code is downloaded.

1. Install the [Python Debugger VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy).

2. Include the following in your `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Remote Attach",
      "type": "python",
      "request": "attach",
      "connect": { "host": "localhost", "port": 5678 },
      "pathMappings": [
        { "localRoot": "${workspaceFolder}", "remoteRoot": "." }
      ],
      "justMyCode": true
    }
  ]
}
```

3. At the top of your Mesop app (e.g. main.py), including the following snippet to start the debug server:

```py
import debugpy

debugpy.listen(5678)
```

4. Connect to your debug server by going to the Run & Debug tab in VS Code and selecting "Python: Remote Attach".

Congrats you are now debugging your Mesop app!

To learn more about Python debugging in VS code, read VS Code's [Python debugging guide](https://code.visualstudio.com/docs/python/debugging).
