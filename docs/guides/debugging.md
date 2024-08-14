# Debugging

This guide will show you several ways of debugging your Mesop app:

- [Debugging with server logs](#debugging-with-server-logs)
- [Debugging with Chrome DevTools](#debugging-with-chrome-devtools)
- [Debugging with VS Code](#debugging-with-vs-code)

You can use the first two methods to debug your Mesop app both locally and in production, and the last one to debug your Mesop app locally.

## Debugging with server logs

If your Mesop app is not working properly, we recommend checking the server logs first.

If you're running Mesop locally, you can check the terminal. If you're running Mesop in production, you will need to use your cloud provider's console to check the logs.

## Debugging with Chrome DevTools

[Chrome DevTools](https://developer.chrome.com/docs/devtools) is a powerful set of web developer tools built directly into the Google Chrome browser. It can be incredibly useful for debugging Mesop applications, especially when it comes to inspecting the client-server interactions.

Here's how you can use Chrome DevTools to debug your Mesop app:

1. Open your Mesop app in Google Chrome.

1. Right-click anywhere on the page and select "Inspect" or use the keyboard shortcut to open Chrome DevTools:
    - Windows/Linux: Ctrl + Shift + I
    - macOS: Cmd + Option + I

1. To debug general errors:
    - Go to the Console tab.
    - Look for any console error messages.
    - You can also modify the [log levels](https://developer.chrome.com/docs/devtools/console/reference#level) to display Mesop debug logs by clicking on "Default levels" and selecting "Verbose".

1. To debug network issues:
    - Go to the [Network tab](https://developer.chrome.com/docs/devtools/network/overview).
    - Reload your page to see all network requests.
    - Look for any failed requests (they'll be in red).
    - Click on a request to see detailed information about headers, response, etc.

1. For JavaScript errors:
   - Check the Console tab for any error messages.
   - You can set breakpoints in your JavaScript code using the Sources tab.

Remember, while Mesop abstracts away much of the frontend complexity, using these tools can still be valuable for debugging and optimizing your app's performance.

## Debugging with VS Code

VS Code is recommended for debugging your Mesop app, but you can also debug Mesop apps in other IDEs.

**Pre-requisite:** Ensure VS Code is downloaded.

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
