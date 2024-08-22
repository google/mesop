"""
This script lists all HTML files in the site directory and writes the list to a text file.

Pre-requisite:

Run `mkdocs build` beforehand to build the docs site.
"""

import os


def list_html_files(directory: str) -> list[str]:
  html_files: list[str] = []
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".html"):
        html_files.append(os.path.join(root, file))
  return html_files


def main():
  directory = "../../site"

  html_files = list_html_files(directory)

  with open("./html_docs_context.txt", "w") as f:
    for file in html_files:
      f.write(f"{file}\n")

  print(
    f"Found {len(html_files)} HTML files. List written to html_docs_context.txt"
  )


if __name__ == "__main__":
  main()
