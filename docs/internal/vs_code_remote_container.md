# VS Code Remote Container

> Git credentials need to be setup in order to commit changes inside the remote
container using VS Code.

VS Code Remote Containers is a quick way to get started with internal Mesop
development if you have [VS Code](https://code.visualstudio.com/) and
[Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

This approach will create a fully configured workspace, saving you time from
debugging installation issues and allowing you to start development right away.

## Pre-requistes: Install VS Code and Docker

In order to use VS Code remote containers, you will need VS Code installed. You will
also need Docker Desktop (which will install Docker Engine and Docker Compose) to run
the remote containers.

- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Open folder in container

Open VS Code, press `Cmd/Ctrl + Shift + P`, and select the `Dev Containers: Open Folder in Container...`
option. This will create a new workspace inside a remote container.

![VS Code open folder in container](../assets/remote-container/open-folder-container.png)

## Wait for postCreateCommand to run

The workspace will not be usable until the `postCreateCommand` has completed.

![Post Create Command](../assets/remote-container/post-create-command.png)

## Run Mesop for development

Once the `postCreateCommand` has finished, you can now start Mesop in the terminal.

```
./scripts/cli.sh
```

You will see some warning messages, but it is OK to ignore them.

You should see this message once the Mesop server is ready.

![Server started](../assets/remote-container/server-start.png)

## View Mesop demos

Once `./scripts/cli.sh` has started the Mesop dev server, you can view the demos at
http://localhost:32123.
