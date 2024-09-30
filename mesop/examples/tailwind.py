"""
Example Tailwind command:

```
npx tailwindcss -i ./tailwind_input.css -o ./tailwind.css
```

Example Tailwind config:

```
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

Original HTML mark up:

```
<html>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-gray-800 text-white py-4">
        <div class="container mx-auto">
            <h1 class="text-2xl font-bold">Header</h1>
        </div>
    </header>

    <!-- Main Content with Sidebar -->
    <div class="flex flex-1">
        <!-- Sidebar -->
        <aside class="w-64 bg-gray-200 p-4">
            <h2 class="text-lg font-semibold mb-4">Sidebar</h2>
            <ul>
                <li><a href="#" class="text-gray-700 block py-2">Link 1</a></li>
                <li><a href="#" class="text-gray-700 block py-2">Link 2</a></li>
                <li><a href="#" class="text-gray-700 block py-2">Link 3</a></li>
            </ul>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 p-6 bg-gray-100">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white p-6 rounded shadow">
                    <h2 class="text-xl font-bold mb-2">Box 1</h2>
                    <p>This is the content for box 1.</p>
                </div>
                <div class="bg-white p-6 rounded shadow">
                    <h2 class="text-xl font-bold mb-2">Box 2</h2>
                    <p>This is the content for box 2.</p>
                </div>
                <div class="bg-white p-6 rounded shadow">
                    <h2 class="text-xl font-bold mb-2">Box 3</h2>
                    <p>This is the content for box 3.</p>
                </div>
            </div>
        </main>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-4">
        <div class="container mx-auto">
            <p>&copy; 2024 Your Company</p>
        </div>
    </footer>

</body>
</html>
```
"""

import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  stylesheets=[
    # Specify your Tailwind CSS URL here.
    #
    # For local testing, you can just launch a basic Python HTTP server:
    #   python -m http.server 8000
    "http://localhost:8000/assets/tailwind.css",
  ],
  path="/tailwind",
)
def app():
  with me.box(classes="min-h-screen flex flex-col"):
    with me.box(classes="bg-gray-800 text-white py-4"):
      with me.box(classes="container mx-auto"):
        with me.box(classes="text-2xl font-bold"):
          me.text("Header")

    with me.box(classes="flex flex-1"):
      with me.box(classes="w-64 bg-gray-200 p-4"):
        with me.box(classes="text-lg font-semibold mb-4"):
          me.text("Sidebar")
        with me.box(classes="text-gray-700 block py-2"):
          me.text("Link 1")
        with me.box(classes="text-gray-700 block py-2"):
          me.text("Link 2")
        with me.box(classes="text-gray-700 block py-2"):
          me.text("Link 3")

      with me.box(classes="flex-1 p-6 bg-gray-100"):
        with me.box(classes="grid grid-cols-1 md:grid-cols-3 gap-4"):
          with me.box(classes="bg-white p-6 rounded shadow"):
            with me.box(classes="text-xl font-bold mb-2"):
              me.text("Box 1")
            me.text("This is the content for box 1.")

          with me.box(classes="bg-white p-6 rounded shadow"):
            with me.box(classes="text-xl font-bold mb-2"):
              me.text("Box 2")
            me.text("This is the content for box 2")

          with me.box(classes="bg-white p-6 rounded shadow"):
            with me.box(classes="text-xl font-bold mb-2"):
              me.text("Box 3")
            me.text("This is the content for box 3")

    with me.box(classes="bg-gray-800 text-white py-4"):
      with me.box(classes="container mx-auto"):
        me.text("2024 Mesop")
