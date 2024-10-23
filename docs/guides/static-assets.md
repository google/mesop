# Static Assets

Mesop allows you to specify a folder for storing static assets that will be served by
the Mesop server.

## Enable a static folder

This feature can be enabled using environment variables.

- [MESOP_STATIC_FOLDER](../api/config.md#mesop_static_folder)
- [MESOP_STATIC_URL_PATH](../api/config.md#mesop_static_folder)

Full description of these two settings can be found on the [config page](../api/config.md).

### Enabling a static folder named "assets"

This will make the files in the `assets` directory accessible from the Mesop server
at `/static`.

Mesop will look for the `assets` directory relative to your application directory.

```bash
MESOP_STATIC_FOLDER=assets mesop main.py
```

### Enabling a static folder named "assets" and URL path of /assets

This will make the files in the `assets` directory accessible from the Mesop server
at `/assets`.

```bash
MESOP_STATIC_FOLDER=assets MESOP_STATIC_URL_PATH=/assets mesop main.py
```

### Using a .env file

You can also specify the environment variables in a `.env` file at the root of your
application directory.

``` title=".env"
MESOP_STATIC_FOLDER=assets
MESOP_STATIC_URL_PATH=/assets
```

Then you can run the Mesop command like this:

```bash
mesop main.py
```

### Example use cases

Here are a couple examples that use the static assets feature.

## Add a logo

This example shows you how to load an image to use as a logo for your app.

Let's assume you have a directory like this:

- static/logo.png
- main.py
- requirements.txt

Then you can reference your logo in your Mesop app like this:

```python title="main.py"
import mesop as me

@me.page()
def foo():
  me.image(src="/static/logo.png")
```

## Load a Tailwind stylesheet

This example shows you how to use [Tailwind CSS](https://tailwindcss.com/) with Mesop.

Let's assume you have a directory like this:

- static/tailwind.css
- tailwind_input.css
- tailwind.config.js
- main.py
- requirements.txt


You can import the CSS into your page using the `stylesheets` parameter on `@me.page`.

```python title="main.py"
import mesop as me

@me.page(stylesheets=["/static/tailwind.css"])
def foo():
  with me.box(classes="bg-gray-800"):
    me.text("Mesop with Tailwind CSS.")
```

Tailwind is able to extract the CSS properties from your Mesop main.py file. This does
not work for all cases. If you have dynamic properties, then you may need to maintain
a safelist as well.

```js title="tailwind.config.js"
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["main.py"],
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [],
};
```

This is just the base Tailwind input file.

```css title="tailwind_input.css"
@tailwind base;
@tailwind components;
@tailwind utilities;
```

The command to generate the output Tailwind CSS is:

```bash
# This assumes you have the tailwindcss CLI installed. If not, see
# https://tailwindcss.com/docs/installation
npx tailwindcss -i ./tailwind_input.css -o ./static/tailwind.css
```
