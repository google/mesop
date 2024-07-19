# Comparison with Other Python UI Frameworks

This page aims to provide an objective comparison between Mesop and other popular Python-based web application frameworks, specifically Streamlit and Gradio. This is a difficult doc to write but we feel that it's important to explain the differences as this is frequently asked.

 While we believe Mesop offers a [unique philosophy for building UIs](https://google.github.io/mesop/blog/2024/05/13/why-mesop/), we strive to be fair and accurate in highlighting the strengths of each framework.

 Because this is a fast-moving space, some of the information may be out of date. Please file an [issue](https://github.com/google/mesop/issues/new/choose) and let us know what we should fix.

## Streamlit

Streamlit and Mesop share similar goals in terms of enabling Python developers to rapidly build web apps, particularly for AI use cases.

However, there are some key differences:

### Execution Model

Streamlit executes apps in a [script-like manner](https://docs.streamlit.io/get-started/fundamentals/main-concepts#data-flow) where the entire app reruns on each user interaction. This enables a boilerplate-free UI development model that's easy to get started with, but requires using mechanisms like [caching](https://docs.streamlit.io/develop/concepts/architecture/caching) and [fragments](https://docs.streamlit.io/develop/concepts/architecture/fragments) to mitigate the performance issues with this model.

Mesop uses a component-based model similar to web frameworks where the program is executed once on server initialization and then the component functions are executed in each render loop. This provides finer-grained control because global initialization code is executed exactly once.

### Styling and Customization

Streamlit provides a set of pre-styled components with limited UI customizability using [themes](https://docs.streamlit.io/develop/concepts/configuration/theming). This ensures a consistent look but can be restrictive for custom designs.

Mesop provides a low-level [Style](./api/style.md) that exposes CSS properties through a Python API. Mesop currently does not provide theming support.

### Components

While Streamlit and Mesop contain many similar standard components (e.g. form, table, chat), Streamlit has a larger set of built-in components, particularly for data science use cases such as data visualization.

Streamlit has a larger ecosystem of community-developed components, while Mesop has a much more nascent community.

## Gradio

Gradio and Mesop both focus on enabling rapid ML/AI app development but with different approaches.

Gradio has a strong focus on creating demos and interfaces for machine learning models and makes it very easy to build a UI for a model.

Mesop, while well-suited for ML/AI use cases, is a more general-purpose framework that can be used for a wider range of web applications.

### Customization and Flexibility

Gradio provides a set of pre-built components optimized for common ML inputs and outputs (e.g. image classification, text generation). This makes it very fast to set up standard model interfaces.

Although Mesop offers a few AI-specific components like [chat](./components/chat.md), Mesop is focused on providing general-purpose UI components which offers greater flexibility in layout and UI design. This makes it better suited for building custom interfaces.

### Deployment

Gradio makes it very easy to share demos via Hugging Face Spaces. Mesop apps can also be deployed on Hugging Face Spaces albeit with a [few more steps](./guides/deployment.md#hugging-face-spaces).

### State Management

Gradio has a simple state management system focused on passing inputs to models and displaying outputs.

Mesop provides a more comprehensive state management solution, allowing for complex application logic and multi-step workflows.

## Learning Curve

Both Streamlit and Gradio have a gentle learning curve, making it very easy for Python developers to get started quickly.

Mesop requires understanding more concepts like event handling to get started, but it offers more flexibility in return. Its API aims to be intuitive for Python developers while introducing modern web development patterns.

## Scale and Ecosystem

Streamlit and Gradio both have larger, more established ecosystems due to their earlier entry into the market. They offer more pre-built components and integrations specific to data science workflows.

Mesop is newer but growing quickly. It benefits from leveraging the mature Angular ecosystem for its frontend, while providing a Python-centric development experience. Mesop's architecture makes it well-suited for larger, more complex applications as well as simple prototypes.

## Conclusion

Ultimately, the best choice depends on your specific use case, desired level of customization, and development experience. We encourage you to try out each framework and see which fits your workflow best.
