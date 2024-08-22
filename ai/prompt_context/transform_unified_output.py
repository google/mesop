"""
Concats the refined output into a single file

Pre-requisite:

Run `python transform_txt.py` first to generate the refined outputs
"""

import os


def concat_refined_outputs():
  input_dir = "../gen/refined_text"
  output_file = "../gen/refined_text_all.txt"

  # Get all .txt files in the input directory
  txt_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
  txt_files = [os.path.join(input_dir, f) for f in txt_files]

  # Sort the files to ensure consistent order
  txt_files.sort()

  with open(output_file, "w", encoding="utf-8") as outfile:
    for file_path in txt_files:
      with open(file_path, encoding="utf-8") as infile:
        outfile.write(infile.read())
      # Append a newline between files for better readability
      outfile.write("\n\n")

    # Append the concat_demo.txt file to the output file
    concat_demo_path = "../gen/concat_demo.txt"
    if os.path.exists(concat_demo_path):
      with open(concat_demo_path, encoding="utf-8") as concat_demo_file:
        outfile.write(
          "I'm going to show you a few example Mesop apps that you can learn from:"
        )
        outfile.write(concat_demo_file.read())
      print(f"Appended content from {concat_demo_path}")
    else:
      print(
        f"Warning: {concat_demo_path} not found. Skipping append operation."
      )

    print(f"All refined outputs have been concatenated into {output_file}")


if __name__ == "__main__":
  concat_refined_outputs()
