# Comparison with Other Python UI Frameworks

This page aims to provide an objective comparison between Mesop and other popular Python-based web application frameworks, specifically Streamlit and Gradio. This is a difficult doc to write but we feel that it's important to explain the differences as this is frequently asked.

 While we believe Mesop offers a [unique philosophy for building UIs](https://google.github.io/mesop/blog/2024/05/13/why-mesop/), we strive to be fair and accurate in highlighting the strengths of each framework.

 Because this is a fast-moving space, some of the information may be out of date. Please file an [issue](https://github.com/google/mesop/issues/new/choose) and let us know what we should fix.

## Streamlit

Streamlit and Mesop share similar goals in terms of enabling Python developers to rapidly build web apps, particularly for AI use cases.

However, there are some key differences:

### Execution Model

Streamlit executes apps in a [script-like manner](https://docs.streamlit.io/get-started/fundamentals/main-concepts#data-flow) where the entire app reruns on each user interaction. This enables a boilerplate-free UI development model that's easy to get started with, but requires mechanisms like [caching](https://docs.streamlit.io/develop/concepts/architecture/caching) and [fragments](https://docs.streamlit.io/develop/concepts/architecture/fragments) to optimize the performance with this model.

Mesop uses a function-based model commonly found in web frameworks where the program is executed once on server initialization and then the page and component functions are executed in each render loop. This provides regular Python execution semantics because top-level initialization code is executed exactly once.

### Styling and Customization

Streamlit provides a set of pre-styled components with limited UI customizability using [themes](https://docs.streamlit.io/develop/concepts/configuration/theming). Streamlit offers pre-styled components with customization primarily through themes, prioritizing consistency and ease of use over flexibility.

In addition to providing, Material-themed components, Mesop provides a low-level [Style](./api/style.md) that exposes CSS properties through a Python API. Mesop currently provides [limited theming support](./guides/theming.md) with dark theming, but doesn't yet [support theming to other colors](https://github.com/google/mesop/issues/669).

### Components

While Streamlit and Mesop contain many similar standard components (e.g. form, table, chat), Streamlit has a larger set of built-in components, particularly for data science use cases such as data visualization.

Streamlit has a larger ecosystem of community-developed components, while Mesop has a more nascent community.

## Gradio

Gradio and Mesop both focus on enabling rapid ML/AI app development but with different approaches.

Gradio has a strong focus on creating demos and interfaces for machine learning models and makes it easy to build a UI for a model.

Mesop, while well-suited for ML/AI use cases, is a more general-purpose framework that can be used for a wider range of web applications.

### Customization and Flexibility

Gradio provides a set of pre-built components optimized for common ML inputs and outputs (e.g. image classification, text generation). This makes it fast to set up standard model interfaces. Gradio has a powerful [theming system](https://www.gradio.app/guides/theming-guide) that provides prebuilt theme options and many options for customizing the UI theme.

Although Mesop offers a few AI-specific components like [chat](./components/chat.md), Mesop provides general-purpose UI components, which can be used for a variety of layout and UI designs. This makes it better suited for building custom interfaces, for example like the [demo gallery](https://google.github.io/mesop/demo/).

### Deployment

Gradio makes it easy to share demos via Hugging Face Spaces. Mesop apps can also be deployed on Hugging Face Spaces, but it requires a [few more steps](./guides/deployment.md#hugging-face-spaces).

### State Management

Gradio provides an imperative approach to [state management](https://www.gradio.app/guides/state-in-blocks) where state is managed together with components.

Mesop provides a more declarative approach to [UI state management](guides/state_management.md) by separating application state updates from component rendering. Mesop also uses a dataclass-based approach managing state which provides type-safety and more structure for managing complex states.

## Conclusion

Both Streamlit and Gradio have a gentle learning curve and make it easy for Python developers to get started quickly.

Mesop introduces concepts like event handling and state management, which can provide additional control and flexibility for more complex applications. Its API aims to be intuitive for Python developers while introducing modern web development patterns.

Ultimately, the best choice depends on your specific use case, desired level of customization, and development experience. We encourage you to try out each framework and see which fits your use case best.
