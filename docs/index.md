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
      Mesop
      <div class="mascot-subtext">
        Build delightful demos quickly in Python
      </div>
    </div>
  </div>
</div>

<div class="mascot-image-spacer"></div>

Mesop is a Python-based UI framework that allows you to rapidly build web demos:


<div class="box-row">
  <div class="reason-box">
    <div class="reason-title">Intuitive for UI novices</div>
    <ul>
      <li>Write UI in <a href="#demo">idiomatic Python code</a></li>
      <li>Easy to understand reactive UI paradigm</li>
      <li>Ready to use <a href="./components/text_io/">components</a></li>
    </ul>
  </div>
  <div class="reason-box">
    <div class="reason-title">Frictionless developer workflows</div>
    <ul>
      <li><b>Hot reload</b> so the browser automatically reloads and preserves state</li>
      <li>Edit your UI code directly in the browser using the visual editor <em>(see below)</em></li>
    </ul>
  </div>
  <div class="reason-box">
    <div class="reason-title">Flexible for delightful demos</div>
    <ul>
      <li>Build custom UIs <em>without</em> writing Javascript/CSS/HTML</li>
      <li>Compose your UI into <a href="./guides/components/">components</a>, which are just Python functions</li>
    </ul>
  </div>
</div>

 <div class="video-container">

<iframe width="560" height="315" src="https://www.youtube.com/embed/tvbO-Lqq_TA?si=bf5pTMneieRLisMc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe><!-- <div>Visual Editor</div>
</div>!-->
</div>

## Demo

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
$ python main.py
```

Learn more in [Getting Started](./getting_started.md).

## Disclaimer

_This is not an officially supported Google product._
