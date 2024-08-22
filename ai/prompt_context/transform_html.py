"""
This script extracts text from HTML files and writes the text to a file.

Pre-requisite:

Run `python transform_docs.py` before running this script.
"""

import os

from bs4 import BeautifulSoup


def extract_text_from_html(file_path: str) -> str:
  with open(file_path, encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")
    article = soup.find("article")
    if article:
      # Preserve original whitespace for code blocks
      for code in article.find_all("code"):  # type: ignore
        code.replace_with(f"\n{code.get_text(strip=False)}\n")  # type: ignore

      # Extract text with preserved code block formatting
      return article.get_text(separator=" ", strip=True)
    else:
      raise Exception(f"No article tag found in {file_path}")


def main():
  input_file = "html_docs_context.txt"
  output_dir = "../gen/extracted_text"  # The directory where we'll store all the extracted text files

  os.makedirs(output_dir, exist_ok=True)

  total_char_count = 0
  processed_files = 0

  with open(input_file) as infile:
    for line in infile:
      line = line.strip()
      if line and not line.startswith("#"):
        try:
          text_content = extract_text_from_html(line)
          output_file = os.path.join(output_dir, f"{line.replace('/','_')}.txt")
          print("output_file", output_file)

          with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(text_content)

          char_count = len(text_content)
          total_char_count += char_count
          processed_files += 1
          print(f"Processed {line}: {char_count} characters")
        except Exception as e:
          print(f"Error processing {line}: {e!s}")

  print(f"Text extraction complete. Output written to {output_dir}")
  print(f"Total files processed: {processed_files}")
  print(f"Total characters extracted: {total_char_count}")


if __name__ == "__main__":
  main()
