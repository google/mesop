import os

# Specify the output file name
output_file = "./gen/prompt_context/api_docs.txt"

with open(output_file, "w", encoding="utf-8") as file:
  file.write("")


# Function to process each .md file
def process_file(file_path: str):
  with open(file_path, encoding="utf-8") as file:
    content = file.read()
    # Don't append empty files
    if len(content.strip()):
      # Remove markdown meta section delimited by ---
      content_lines = content.split("\n")
      in_meta_section = False
      filtered_content: list[str] = []

      for line in content_lines:
        if line.strip() == "---":
          in_meta_section = not in_meta_section
          continue
        if not in_meta_section:
          filtered_content.append(line)

      content = "\n".join(filtered_content)
      url = ""
      if file_path.startswith("../docs/"):
        file_path = file_path.replace(
          "../docs/", "https://google.github.io/mesop/"
        ).replace(".md", "/")
        # https://google.github.io/mesop/
        url = file_path

      with open(output_file, "a", encoding="utf-8") as output:
        output.write(f"<page url='{url}'>\n")
        output.write(content)
        output.write("</page>\n\n")


def crawl(path: str, ext: str):
  for root, dirs, files in os.walk(path):
    new_dirs: list[str] = []
    for dir in dirs:
      print("dir", dir, "path", path)
      if dir == "components" and path == "../docs":
        continue
      if dir not in ["venv", "__pycache__", "internal", "blog"]:
        new_dirs.append(dir)
    dirs[:] = new_dirs
    for file in files:
      # These files have a lot of HTML / not very good for context.
      if path == "../docs" and file in ["demo.md", "index.md"]:
        continue
      if file.endswith(ext):
        file_path = os.path.join(root, file)
        process_file(file_path)


with open(output_file, "a", encoding="utf-8") as output:
  output.write(
    "I will teach you how to use a Python UI framework called Mesop:\n\n"
  )
crawl(path="../docs", ext=".md")

with open(output_file, "a", encoding="utf-8") as output:
  output.write("These are all the components and their APIs:")
crawl(path="../mesop/labs", ext=".py")
crawl(path="../mesop/components", ext=".py")
crawl(path="../mesop/component_helpers", ext="style.py")

with open(output_file, "a", encoding="utf-8") as output:
  output.write("These are example applications you can build with Mesop:")
crawl(path="../demo", ext=".py")

with open(output_file, encoding="utf-8") as output:
  output_length = len(output.read())

print(f"Generated prompt: {output_file} | length={output_length}")
