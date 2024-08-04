---
date: 2024-07-12
---

# Is Mesop + Web Components the cure to Front-end fatigue?

I saw this tweet the other day and couldn't help but chuckle:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">is this the thing that will finally save me from ever learning front end?<a href="https://t.co/eDgY0AfG6U">https://t.co/eDgY0AfG6U</a></p>&mdash; xlr8harder (@xlr8harder) <a href="https://twitter.com/xlr8harder/status/1798673386425786724?ref_src=twsrc%5Etfw">June 6, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

At first, I thought of it as joke, but now that Mesop has launched experimental support for [Web Components](https://google.github.io/mesop/web-components/), I think it's plausible that Mesop with Web Components can save you from front-end fatigue.

## What is Mesop?

Before we dive in, let me explain what Mesop is. Mesop is a Python UI framework focused on rapidly building AI apps. You can write a lot of kinds of apps all in Python as you can see from the examples on our [home page](https://google.github.io/mesop/), but when you need to, Mesop provides the flexibility of dropping down into web components so you can  have fine-grained UI control and use existing JS libraries.

## Avoid the builds

![Programming meme](https://i.redd.it/tfugj4n3l6ez.png)

DHH, creator of Rails, recently gave an [interview](https://youtu.be/rEZNbM4MUdo?si=e0uk-2DsCvwwFVHO&t=1485) saying how he's "done with bundling" and the overall complexity of modern front-end build toolchains.

As someone who's done front-end for almost a decade, I can attest to the sentiment of feeling the pain of compiling JavaScript options. Setting up compiler configs and options can easily take hours. I want to be clear, I think a lot of these tools like TypeScript are fantastic, and the core Mesop framework itself is compiled using TypeScript and Angular's compilers.

But when it comes to rapid prototyping, I want to avoid that overhead. In our [design proposal](https://docs.google.com/document/d/1Nc7Ub8DMNSxAmFuPRdyrlZXh_AoxVjZM-YEeWF8dAyI/edit#heading=h.36b20xkar02d), we intentionally designed a lightweight model where you don't _need_ to set up a complex build chain to start writing JavaScript.

Sometimes a build step is unavoidable, e.g. you're writing TypeScript, and you can still compile your JavaScript as needed.

## Framework churn

The front-end ecosystem is infamous for its steady and constant churn. The good thing about building on top of web components is that it's based on [web standards](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) supported by all modern browsers. This means, that given browser makers' focus on "not breaking the web", this will be there for many years, if not decades to come.

For years, web components had a reputation of being an immature technology due to inconsistent support across browsers, but fast forward to 2024, and web components are well-supported in modern browsers and libraries built on web components like [Lit](https://lit.dev/), which is downloaded millions of times a week.

## Minimizing front-end fatigue in Mesop

FE developers are so used to the pain and complexity of front-end development that they can forget how steep the learning curve is until someone from another domain tries to build a simple web app, and struggles with just getting the web app up and started.

Mesop app developers are mostly _not_ front-end developers which means that reducing the complexity, especially learning curve, of building custom components is very important. In Mesop, we've designed a smooth pathway where you can [get started](https://google.github.io/mesop/web-components/quickstart/) with a little front-end knowledge and build simple custom components without learning a complex front-end framework.

## What's next

Follow [our X/Twitter account, @mesop_dev](https://x.com/mesop_dev) for more updates. We're working on improving our web component support, in particular by:

- Creating guides for wrapping React components into Mesop web components
- Fostering an ecosystem of open-source Mesop web components by making it easy to discover and reuse web components that other people have built.

We're excited about the potential of Mesop and Web Components to simplify front-end development. Whether it's the cure for front-end fatigue remains to be seen, but I think it offers a promising alternative to the complexity of traditional front-end development.
