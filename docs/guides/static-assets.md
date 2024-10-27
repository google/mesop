# Static Assets

Mesop allows you to specify a folder for storing static assets that will be served by
the Mesop server.

This feature provides a simple way to serving images, favicons, CSS stylesheets, and
other files without having to rely on CDNs, external servers, or mounting Mesop onto
FastAPI/Flask.

## Enable a static folder

This feature can be enabled using environment variables.

- [MESOP_STATIC_FOLDER](../api/config.md#mesop_static_folder)
- [MESOP_STATIC_URL_PATH](../api/config.md#mesop_static_url_path)

Full descriptions of these two settings can be found on the [config page](../api/config.md).

### Enabling a static folder named "assets"

This will make the files in the `assets` directory accessible from the Mesop server
at `/static`.

Mesop will look for the `assets` directory relative to your current working directory.
In this case, `/some/path/mesop-app/assets`.

```bash
cd /some/path/mesop-app
MESOP_STATIC_FOLDER=assets mesop main.py
```

Here is another example:

Mesop will look for the `assets` directory relative to your current working directory.
In this case, `/some/path/assets`.

```bash
cd /some/path
MESOP_STATIC_FOLDER=assets mesop mesop-app/main.py
```
### Enabling a static folder named "assets" and URL path of /assets

This will make the files in the `assets` directory accessible from the Mesop server
at `/assets`. For example: `https://example.com/assets`.

```bash
MESOP_STATIC_FOLDER=assets MESOP_STATIC_URL_PATH=/assets mesop main.py
```

### Using a .env file

You can also specify the environment variables in a `.env` file. This file should be
placed in the same directory as the `main.py` file.

``` title=".env"
MESOP_STATIC_FOLDER=assets
MESOP_STATIC_URL_PATH=/assets
```

Then you can run the Mesop command like this:

```bash
mesop main.py
```

## Example use cases

Here are a couple examples that use the static assets feature.

### Add a logo

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

### Use a custom favicon

This example shows you how to use a custom favicon in your

Let's assume you have a directory like this:

- static/favicon.ico
- main.py
- requirements.txt

If you have a static folder enabled, Mesop will look for a `favicon.ico` file in your
static folder. If the file exists, Mesop will use your custom favicon instead of the
default Mesop favicon.

### Load a Tailwind stylesheet

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
not work for all cases. If you are dynamically generating CSS properties using string concatenation/formatting, then Tailwind may not be able to determine which properties
to include. In that case, you may need to manually add these classes to the safelist.

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
