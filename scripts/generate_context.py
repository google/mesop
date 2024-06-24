import os

# Specify the output file name
output_file = "./scripts/gen/prompt_preamble.txt"

with open(output_file, "w", encoding="utf-8") as file:
  file.write("")


# Function to process each .md file
def process_file(file_path: str):
  with open(file_path, encoding="utf-8") as file:
    content = file.read()
    # Don't append empty files
    if len(content.strip()):
      with open(output_file, "a", encoding="utf-8") as output:
        output.write(f"--- {file_path} \n")
        output.write(content)
        output.write("\n\n")


def crawl(path: str, ext: str):
  for root, dirs, files in os.walk(path):
    new_dirs: list[str] = []
    for dir in dirs:
      if dir != "venv" and dir != "__pycache__":
        new_dirs.append(dir)
    dirs[:] = new_dirs
    for file in files:
      if file.endswith(ext):
        file_path = os.path.join(root, file)
        process_file(file_path)


with open(output_file, "a", encoding="utf-8") as output:
  output.write(
    "I will teach you how to use a Python UI framework called Mesop:"
  )
crawl(path="./docs", ext=".md")
# crawl(path="./docs/guides", ext=".md")
# crawl(path="./docs/components", ext=".md")
with open(output_file, "a", encoding="utf-8") as output:
  output.write("These are all the components and their APIs:")
crawl(path="./mesop/labs", ext=".py")
crawl(path="./mesop/components", ext=".py")
crawl(path="./mesop/component_helpers", ext="style.py")
with open(output_file, "a", encoding="utf-8") as output:
  output.write("These are example applications you can build with Mesop:")
crawl(path="./demo", ext=".py")

with open(output_file, encoding="utf-8") as output:
  output_length = len(output.read())

print(f"Generated prompt: {output_file} | length={output_length}")
