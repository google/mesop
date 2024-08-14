# Frequently Asked Questions

## General

### What kinds of apps is Mesop suited for?

Mesop is well-suited for ML/AI demos and internal tools because it enables developers without frontend experience to quickly build web apps. For use cases that prioritize developer experience and velocity, Mesop can be a good choice.

Demanding consumer-facing apps, which have strict requirements in terms of performance, custom UI components, and i18n/localization would not be a good fit for Mesop and other UI frameworks may be more suitable.

### How does Mesop compare to other Python UI frameworks?

We have written a [comparison](./comparison.md) doc to answer this question in-depth.

### Is Mesop production-ready?

Dozens of teams at Google have used Mesop to build demos and internal apps.

Although Mesop is pre-v1, we take backwards-compatibilty seriously and avoid backwards incompatible change. This is critical to us because many teams within Google rely on Mesop and we need to not break them.

Occasionally, we will do minor clean-up for our APIs, but we will provide warnings/deprecation notices and provide at least 1 release to migrate to the newer APIs.

### Which modules should I import from Mesop?

Only import from these two modules:

```py
import mesop as me
import mesop.labs as mel
```

All other modules are considered internal implementation details and may change without notice in future releases.

### Is Mesop an official Google product?

No, Mesop is not an official Google product and Mesop is a 20% project maintained by a small core team of Google engineers with contributions from the broader community.

## Deployment

### How do I share or deploy my Mesop app?

The best way to share your Mesop app is to deploy it to a cloud service. You can follow our [deployment guide](./guides/deployment.md) for step-by-step instructions to deploy to Google Cloud Run.

> Note: you should be able to deploy Mesop on any cloud service that takes a container. Please read the above deployment guide as it should be similar steps.
