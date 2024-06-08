---
hide:
  - navigation
  - toc
---
<!-- Hide page title -->
<style>
  .md-typeset h1 {
    display: none;
  }
</style>

<div class="mascot-image-container">
  <img class="mascot-image" src="./assets/robot_mascot.jpeg"/>
  <div class="mascot-text-container">
    <div class="mascot-text">
      Quickly build web UIs in Python
      <div class="mascot-subtext">
        Used at Google for rapid internal app development
      </div>
    </div>
  </div>
</div>

<div class="mascot-image-spacer"></div>

Mesop is a Python-based UI framework that allows you to rapidly build web apps like demos and internal apps:

<div class="box-row">
  <div class="reason-box">
    <div class="reason-title">Easy to get started</div>
    <ul>
      <li>Write UI in <a href="#demo">idiomatic Python code</a></li>
      <li>Skip the FE learning curve.</li>
      <li>Ready to use components (e.g. <a href="./components/chat/">chat</a>)</li>
    </ul>
  </div>
  <div class="reason-box">
    <div class="reason-title">Fast iteration</div>
    <ul>
      <li><b>Hot reload</b> so the browser automatically reloads and preserves state</li>
      <li>Rich IDE support with strong type safety</li>
    </ul>
  </div>
  <div class="reason-box">
    <div class="reason-title">Flexible & composable</div>
    <ul>
      <li>Build custom UIs <em>without</em> writing Javascript/CSS/HTML</li>
      <li>Compose your UI into <a href="./guides/components/">components</a>, which are just Python functions</li>
    </ul>
  </div>
</div>

<h2 style="margin: 0.5rem"> See what you can build in less than 10 lines of code... </h2>

<iframe class="immersive-demo" src="https://google.github.io/mesop/demo/"></iframe>

Check out how the above [demo gallery](./demo.md) was [built in pure Mesop](https://github.com/google/mesop/blob/main/demo/main.py)!

## Try it

### Colab

Try Mesop on Colab: [![Open In Colab](assets/colab.svg)](https://colab.research.google.com/github/google/mesop/blob/main/notebooks/mesop_colab_getting_started.ipynb)

### Locally

__Step 1:__ Install it

```sh
$ pip install mesop
```

__Step 2:__ Copy the example above into `main.py`

__Step 3:__ Run the app

```sh
$ mesop main.py
```

## Next Steps

Learn more in [Getting Started](./getting_started/installing.md).

## Disclaimer

_This is not an officially supported Google product._
