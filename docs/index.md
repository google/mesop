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
      <li>Skip the pain of learning the FE ecosystem (e.g. npm, compiling) with a single `pip install mesop`</li>
      <li>Ready to use <a href="./components/text_io/">components</a></li>
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

## Write your first Mesop app in less than 10 lines of code...

=== "Demo & Code"



<div class="code-demo">


<iframe class="demo" src="https://mesop-y677hytkra-uc.a.run.app/text_io"></iframe>


```python
--8<-- "mesop/examples/text_io.py"
```

</div>

## Try it

__Step 1:__ Install it

```sh
$ pip install mesop
```

__Step 2:__ Copy the example above into `main.py`

__Step 3:__ Run the app

```sh
$ mesop main.py
```

Learn more in [Getting Started](./getting_started.md).

## Disclaimer

_This is not an officially supported Google product._
