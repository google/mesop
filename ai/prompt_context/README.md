# Prompt Context Generation

This directory contains scripts to generate prompt context for Large Language Models (LLMs) from the Mesop documentation.

## Purpose

The purpose of these scripts is to transform the Mesop documentation into a format that is easily consumable by LLMs. This process involves extracting text from HTML files, refining the content, and creating a condensed yet comprehensive prompt context.

## Scripts and Usage

**Setup**:

First, install the core Python dependencies for the project:

```sh
pip install -r build_defs/requirements_lock.txt
```

- Ensure you have the necessary dependencies installed:
  - BeautifulSoup (`pip install beautifulsoup4`)
  - google.generativeai (`pip install google-generativeai`)
- Set the `GEMINI_FREE_API_KEY` environment variable for the Gemini API used in `transform_txt.py`.

**Usage**:

Follow these steps in order to generate the prompt context:

> Note: These scripts use relative paths, so run them from the `prompt_context` directory.

1. **transform_demo.py**

   - Purpose: Concatenates important demo Python files.
   - Usage: `python transform_demo.py`
   - Output: Creates `../gen/concat_demo.txt` with concatenated demo files.

1. **transform_docs.py**

   - Purpose: Lists all HTML files in the site directory.
   - Prerequisite: Run `mkdocs build` to build the docs site.
   - Usage: `python transform_docs.py`
   - Output: Creates `html_docs_context.txt` with a list of HTML files. This file is generated and then manually edited to commented out files that are not relevant to the prompt context.

1. **transform_html.py**

   - Purpose: Extracts text from HTML files.
   - Usage: `python transform_html.py`
   - Output: Creates text files in the `../gen/extracted_text` directory.

1. **transform_txt.py**

   - Purpose: Refines the extracted text for LLM consumption by calling an LLM.
   - Usage: `python transform_txt.py`
   - Output: Creates refined text files in the `../gen/refined_text` directory.
   - **NOTE**: You will need to manually edit the "style" doc because the LLM doesn't generate a good summary of it.

1. **transform_unified_output.py**
   - Purpose: Concatenates all the refined text files and the demo files.
   - Usage: `python transform_unified_output.py`
   - Output: Creates `../gen/refined_text_all.txt` with the concatenated files.

## Notes

After running these scripts, you'll have a set of refined text files and concatenated demo files that can be used as context for LLMs when working with Mesop.
