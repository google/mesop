import os


def concatenate_py_files():
  output_file = "../gen/concat_demo.txt"

  # Ensure the output directory exists
  os.makedirs(os.path.dirname(output_file), exist_ok=True)

  # Lists the most important demos.
  py_files = [
    "../../demo/main.py",
    "../../demo/llm_rewriter.py",
    "../../demo/llm_playground.py",
    "../../mesop/labs/chat.py",
    "../../mesop/labs/text_to_text.py",
    "../../showcase/main.py",
  ]

  # Sort the files to ensure consistent order
  py_files.sort()

  with open(output_file, "w") as outfile:
    for py_file in py_files:
      filename = os.path.basename(py_file)
      outfile.write(f"<mesop-app='{filename}'>\n\n")

      with open(py_file) as infile:
        outfile.write(infile.read())

      outfile.write("</mesop-app>\n\n")

  print(f"Concatenated files written to {output_file}")


if __name__ == "__main__":
  concatenate_py_files()
