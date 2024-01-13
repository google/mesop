---
date: 2024-01-12
---

# Visual Editor

## Why?

As I began discussing Mesop with friends and colleagues, one thing that has come up is the difficulty of teaching and persuading non-frontend engineers to build UIs, even simple ones. CSS, particularly the rules around layout, can be quite challenging and off-putting.

I've developed a new [visual editor](https://github.com/google/mesop/issues/31) for Mesop that aims to make UI building more approachable for beginners and more productive for experts.

## What?

Let's take a look at the visual editor:

![Visual Editor v1](../../assets/editor-v1.png)

With the visual editor, you can:

- Add new components into your app
- Modify existing components
- Visualize the component tree hierarchy
- You can inspect existing components on the page by hovering over them and then change them in the editor panel
- **B**ring **Y**our **O**wn components. By decorating a Python function with `me.component`, you've turned it into a Mesop component and you can now add it with the visual editor.

What's exciting about the visual editor is that you aren't locked into it - everytime you change a component with the visual editor, it's modifying the source code directly so you can seamlessly go back forth between a regular text editor and the visual editor to build your Mesop app.

## Prior Art

Visual editors (aka WYSIWYG builders) have been around for a long time. [Puck](https://github.com/measuredco/puck) is one of the most interesting ones because of a few reasons: 1) it's open-source, 2) it's flexible (e.g. bring your own components) and 3) it's intuitive and easy-to-use.

The main issues I saw with Puck, particularly for Mesop's use case, is that it [currently only supports React](https://github.com/measuredco/puck/issues/302) (and Mesop uses Angular) and Puck saves data whereas I would like Mesop's Visual Editor to directly emit/update code, which I'll explain next.

## Principles

### Hybrid code (not low-code)

One of the reasons why WYSIWYG builders have not gotten much traction with engineers is that they're often good for simple applications, but then you [hit a wall](https://www.reddit.com/r/FlutterDev/comments/165d804/what_do_you_think_about_flutter_flow/) building more complex applications.

To avoid this issue, I'm focusing on making the Visual Editor actually emit __code__ and _not_ just __data__. Essentially, the UI code that you produce from the Visual Editor should be the same as the code that you would write by hand.

### Unobtrustive UI

I want Mesop app developers to do most of their work (except for the final finetuning for deployment) in the Visual Editior which means that it's important the Editor UI is un-obtrusive. Chrome DevTools is a great example of a low-key tool that many web developers keep open throughout their development - it's helpful for debugging, but then it's out of your way as you're interacting with the application.

Concretely, this means:

- Editor UI should be collapsible
- You should be able to "disable" the editor mode and interact with the application as a normal user.

### Contextual

The visual editor should provide only the information that you need when you need it.

For example, rather than showing all the style properties in the editor panel, which would be quite overwhelming, we only show the style properties that you're using for the selected component.

### Local-only

Because the Visual Editor relies on editing files in your local filesystem, I want to avoid any accidental usages out in the wild. Concretely, this means that you can only use the Visual Editor in localhost, otherwise the Mesop server will reject the editor edit requests.

## What's next

There's still a lot of improvements and polishes I would like to make to the visual editor, but a few high-level ideas that I have are:

1. Build example applications using the visual editor with a video walkthrough.
1. Create more high-level components in Mesop Labs, which I'll introduce in an upcoming blog post, to make it even easier to build apps with the visual editor.
1. Drag and drop components onto the page and within the page. This will provide an intuitive experience for building the UI, literally block by block.
