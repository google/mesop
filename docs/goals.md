# Goals

I think it's helpful to explicitly state the goals of a project because it provides clarity for not only the development team, but also developers who are evaluating Mesop amongst other options:

1. **Prioritize Python developer experience** - Provide the best possible developer experience for Python engineers with minimal frontend experience. Traditional web UI frameworks (e.g. React) prioritize developer experience, but they are focused on web developers who are familiar with the web ecosystem (e.g. HTML, node.js, etc.).
1. **Rich user interactions** - You should be able to build reasonably sophisticated web applications and demos (e.g. LLM chat) without building custom native components.
1. **Simple deployment** - Make deployment simple by packaging Mesop into a container which can be deployed as a standalone server.

## Examples of applying these goals

- **Web performance**: This doesn't mean other goals like web performance have no weight, but we will consistently rank these goals as higher priorities. For example, we could improve performance by serving static assets via CDN, but this would complicate our deployment. For instance, we'd need to ensure that pushing a new Python server binary and JS static assets happened at the same time, or you can get version skews which can cause cryptic errors.

- **Template vs. code**: Mesop adopts the pattern of UI-as-code instead of using a separate templating language. Our belief is that writing Python code is a significantly better learning curve for our target developers. Rather than making them learn a new templating language (DSL) that they are unfamiliar with, they can write Python code which allows them idiomatic ways of expressing conditional logic and looping.
