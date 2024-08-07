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

Streamlit offers pre-styled components with customization primarily through [themes](https://docs.streamlit.io/develop/concepts/configuration/theming), prioritizing consistency and ease of use over flexibility.

In addition to providing Material-themed components, Mesop offers a low-level [Style](./api/style.md) API to configure CSS properties. Mesop provides [limited theming support](./guides/theming.md) with dark theming and doesn't [support theming to other colors](https://github.com/google/mesop/issues/669).

### Components

Both Streamlit and Mesop offer a range of standard components (e.g., forms, tables, chat interfaces), with Streamlit providing a larger set of built-in components, especially for data science use cases like data visualization.

Streamlit supports [custom components](https://docs.streamlit.io/develop/concepts/custom-components/intro) rendered in iframes for isolation. It offers first-class support for React components and can accommodate other frameworks through a framework-agnostic template.

Mesop enables creating custom [web components](./web-components/index.md) based on open web standards, facilitating interoperability with components from different frameworks like Lit. Mesop web components are rendered in the same frame as the rest of the Mesop app which provides more flexibility but less isolation.

Streamlit has a more established ecosystem of community-developed components, while Mesop's community and component ecosystem are still developing.

## Gradio

Gradio and Mesop both enable rapid ML/AI app development but with different approaches.

Gradio has a strong focus on creating demos and interfaces for machine learning models and makes it easy to build a UI for a model. Gradio also offers a lower-level abstraction known as [Blocks](https://www.gradio.app/docs/gradio/blocks) for more general web applications.

Mesop, while well-suited for ML/AI use cases, is a more general-purpose framework that can be used for a wide range of web applications.

### Components

Gradio provides a set of pre-built components optimized for common ML inputs and outputs (e.g. image classification, text generation). This makes it fast to set up standard model interfaces. In addition to built-in components, you can create [custom components](https://www.gradio.app/guides/custom-components-in-five-minutes) in Python and JavaScript (Svelte).

Mesop provides general-purpose UI components, which can be used for a variety of layout and UI designs. Higher-level components like the [chat](./components/chat.md) component are [built](https://github.com/google/mesop/blob/main/mesop/labs/chat.py) on top of these low-level UI components. This makes it better suited for building custom interfaces, such as the [demo gallery](./demo.md). Mesop also supports creating custom [web components](./web-components/index.md) based on open web standards, facilitating interoperability with components from different frameworks.

### Styling and Customization

Gradio features a robust [theming system](https://www.gradio.app/guides/theming-guide) with prebuilt options and extensive UI customization. It also supports [custom CSS](https://www.gradio.app/guides/custom-CSS-and-JS) via direct string construction.

Mesop offers a statically typed [Style](./api/style.md) API for CSS properties. While it includes [dark theme support](./guides/theming.md), Mesop's theming capabilities are currently limited and does not allow custom color schemes.

### State management

Gradio uses an imperative approach to [state management](https://www.gradio.app/guides/state-in-blocks), coupling state with component updates. State is typically managed through function parameters and return values, which can be straightforward for simple interfaces but may become complex as applications grow.

Mesop adopts a declarative [state management](guides/state-management.md) approach, separating state updates from UI rendering. It uses dataclasses for state, providing type-safety and structure for complex states. This separation allows for more granular control over UI updates but may have a steeper learning curve for beginners.

### Deployment

Gradio makes it easy to share demos via Hugging Face Spaces. Mesop apps can also be deployed on Hugging Face Spaces, but requires a [few more steps](./guides/deployment.md#hugging-face-spaces).

## Conclusion

Both Streamlit and Gradio offer gentle learning curves, making it easy for Python developers to quickly build standard AI applications.

Mesop embraces a declarative UI paradigm, which introduces additional concepts but can provide more flexibility for custom applications.

Ultimately, the best choice depends on your specific use case, desired level of customization, and development preferences. We encourage you to explore each framework to determine which best fits your needs.
