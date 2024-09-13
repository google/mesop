import difflib
import re
from typing import NamedTuple

EDIT_HERE_MARKER = " # <--- EDIT HERE"


class ApplyPatchResult(NamedTuple):
  has_error: bool
  result: str


def apply_patch(original_code: str, patch: str) -> ApplyPatchResult:
  # Extract the diff content
  diff_pattern = r"<<<<<<< ORIGINAL(.*?)=======\n(.*?)>>>>>>> UPDATED"
  matches = re.findall(diff_pattern, patch, re.DOTALL)
  patched_code = original_code
  if len(matches) == 0:
    print("[WARN] No diff found:", patch)
    return ApplyPatchResult(
      True,
      "[AI-001] Sorry! Could not find diff in output. Please try again.",
    )
  for original, updated in matches:
    original = original.strip().replace(EDIT_HERE_MARKER, "")
    updated = updated.strip().replace(EDIT_HERE_MARKER, "")

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      return ApplyPatchResult(
        True,
        "[AI-002] Sorry! AI output could not be used. Please try again.",
      )
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


def apply_udiff(original_text: str, udiff: str) -> ApplyPatchResult:
  # Check if the udiff contains code blocks
  if "```" in udiff:
    udiff = extract_code_blocks(udiff)
    print("udiff***\n", udiff)
  lines = original_text.splitlines()
  # Remove extra newline after hunk header which causes an issue
  udiff = udiff.replace("@@\n\n", "@@\n")
  patch_lines = normalize_udiff_lines(udiff.splitlines())
  if "@@" not in udiff:
    print("[WARN] No diff found:", udiff)
    return ApplyPatchResult(
      True,
      "[AI-001] Could not find diff in output. Please try again.",
    )
  try:
    patched_lines = lines.copy()
    hunk_lines = []
    for patch in patch_lines:
      if patch.startswith("@@"):
        if hunk_lines:
          patched_lines = apply_hunk(
            patched_lines,
            # Skip the @@ line
            hunk_lines[1:],
          )
        hunk_lines = [patch]
      else:
        hunk_lines.append(patch)

    if hunk_lines:
      patched_lines = apply_hunk(
        patched_lines,
        # Skip the @@ line
        hunk_lines[1:],
      )

    patched_code = "\n".join(patched_lines)
  except Exception as e:
    print("[WARN] Error applying udiff:", e)
    return ApplyPatchResult(
      True,
      f"[AI-003] Error applying udiff: {e!s}. Please try again.",
    )
  if original_text == patched_code:
    print("[WARN] No changes applied:", udiff)
    return ApplyPatchResult(
      True,
      "[AI-001] No changes were applied. Please try again.",
    )
  return ApplyPatchResult(False, patched_code)


def normalize_udiff_lines(lines: list[str]) -> list[str]:
  normalized_lines = []
  for i, line in enumerate(lines):
    if line == "" and i > 0 and i < len(lines) - 1:
      if lines[i - 1].startswith("+") and lines[i + 1].startswith("+"):
        normalized_lines.append("+")
      elif lines[i - 1].startswith(" ") and lines[i + 1].startswith(" "):
        normalized_lines.append(" ")
      else:
        normalized_lines.append(line)
    else:
      normalized_lines.append(line)
  return normalized_lines


def apply_hunk(lines: list[str], hunk_lines: list[str]) -> list[str]:
  # sections = split_hunk_into_sections(hunk_lines)

  # for section in sections:
  context_before, changes, context_after = process_section(hunk_lines)
  start = find_context(lines, context_before)
  if start == -1:
    raise ValueError(
      "Could not find context in original text", "\n".join(context_before)
    )

  # if context_after:
  #   end = find_context(lines[start + len(context_before) :], context_after)
  #   if end == -1:
  #     raise ValueError(
  #       "Could not find ending context in original text",
  #       "\n".join(context_after),
  #     )
  #   end += start + len(context_before)
  # else:
  end = (
    start
    + len(context_before)
    + sum(1 for line in changes if line.startswith("-"))
  )
  print("context_before")
  print("\n".join(context_before))
  print("changes")
  print("\n".join(changes))
  print("context_after")
  print("\n".join(context_after))

  result = lines[:start]
  result.extend(context_before)

  for change in changes:
    if change.startswith("+") or change.startswith(" "):
      result.append(change[1:])

  count = 0
  for change in changes:
    if change.startswith(" "):
      count += 1
  # result.extend(context_after)

  print("end", end)
  print("count", count)
  print("EXTEND")
  print(lines[end + count :])
  result.extend(lines[end + count :])

  lines = result

  return lines


def split_hunk_into_sections(hunk_lines: list[str]) -> list[list[str]]:
  sections = []
  current_section = []

  for line in hunk_lines:
    if line == "":
      current_section.append(line)
    if (
      line.startswith(" ")
      and not current_section
      or line.startswith(("-", "+"))
    ):
      current_section.append(line)
    elif line.startswith(" ") and current_section:
      if any(l.startswith(("-", "+")) for l in current_section):  # noqa: E741
        sections.append(current_section)
        current_section = [line]
      else:
        current_section.append(line)

  if current_section:
    sections.append(current_section)
  print("sections")
  for section in sections:
    print("section")
    print("\n".join(section))
    print("---")
  return sections


def process_section(section):
  context_before = []
  changes = []
  context_after = []
  in_changes = False

  for line in section:
    if line == "":
      if in_changes:
        changes.append(line)
        context_after.append(line)
      else:
        context_before.append(line)
    elif line.startswith(" "):
      if in_changes:
        changes.append(line)
        # context_after.append(line[1:])
      else:
        context_before.append(line[1:])
    elif line.startswith("-") or line.startswith("+"):
      changes.append(line)
      in_changes = True
  print("***PROCESS SECTION***")
  print("context_before")
  print("\n".join(context_before))
  print("changes")
  print("\n".join(changes))
  print("context_after")
  print("\n".join(context_after))
  return context_before, changes, context_after


def find_context(lines: list[str], context: list[str]) -> int:
  if not context:
    return 0

  # Try different indentation levels
  for indent in range(-4, 4, 1):
    indented_context = [" " * indent + line for line in context]
    context_str = "\n".join(indented_context)
    text = "\n".join(lines)
    index = text.find(context_str)

    if index != -1:
      # replace context with indented context
      context.clear()
      context.extend(indented_context)
      return text[:index].count("\n")

  # If no match found, print debug information and return -1
  print(
    "Could not find context in original text",
    "\ncontext_str",
    "\n".join(context),
    "\nlines",
    "\n".join(lines),
  )
  return -1


def extract_code_blocks(text: str) -> str:
  """
  Extracts and concatenates the content of all code blocks from the given text.

  Args:
  text (str): The input text that may contain code blocks.

  Returns:
  str: A string containing only the content of the code blocks, joined with newlines.
  """
  # Find all code blocks in the text
  code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)

  # Join the content of all code blocks
  return "\n".join(code_blocks)


def create_udiff(source: str, patched: str) -> str:
  """
  Creates a unified diff between the source and patched code.
  """
  diff_lines = list(
    # Need more than 3 lines, otherwise we will get false matches.
    difflib.unified_diff(source.splitlines(), patched.splitlines(), n=5)
  )[2:]

  # Replace markers with @@ .. @@
  diff_lines = [
    re.sub(r"@@ .+ @@", "@@ .. @@", line) if line.startswith("@@") else line
    for line in diff_lines
  ]

  return "\n".join(diff_lines)
