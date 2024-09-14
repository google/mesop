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
  # Remove the edit markers.
  original_text = original_text.replace(EDIT_HERE_MARKER, "")
  udiff = udiff.replace(EDIT_HERE_MARKER, "")
  # Check if the udiff contains code blocks
  if "```" in udiff:
    udiff = extract_code_blocks(udiff)
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
  if original_text.endswith("\n"):
    patched_code = patched_code.rstrip() + "\n"
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
  # Currently we don't use context_after, but we could use it in the future
  # to be more precise if find_context has multiple matches.
  context_before, changes, context_after = process_section(hunk_lines)
  start = find_context(lines, context_before)
  end = (
    start
    + len(context_before)
    + sum(1 for line in changes if line.startswith("-"))
  )

  result = lines[:start]
  result.extend(context_before)

  for change in changes:
    if change.startswith("+") or change.startswith(" "):
      result.append(change[1:])

  result.extend(
    lines[end + sum(1 for change in changes if change.startswith(" ")) :]
  )
  return result


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
      else:
        context_before.append(line[1:])
    elif line.startswith("-") or line.startswith("+"):
      changes.append(line)
      in_changes = True

  return context_before, changes, context_after


def find_context(lines: list[str], context: list[str]) -> int:
  if not context:
    return 0

  # Try different indentation levels because the LLM sometimes
  # messes up the indentation.
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

  raise ValueError(
    "Could not find context in original text\n"
    "context:\n" + "\n".join(context) + "\noriginal:\n" + "\n".join(lines)
  )


def extract_code_blocks(text: str) -> str:
  """
  Extracts and concatenates the content of all code blocks from the given text.
  """
  code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
  return "\n".join(code_blocks)


def create_udiff(*, source: str, patched: str) -> str:
  diff_lines = list(
    # Have 5 lines of context, otherwise we will get incorrect matches.
    difflib.unified_diff(source.splitlines(), patched.splitlines(), n=5)
  )[2:]

  # Replace markers with @@ .. @@
  diff_lines = [
    re.sub(r"@@ .+ @@", "@@ .. @@", line) if line.startswith("@@") else line
    for line in diff_lines
  ]

  return "\n".join(diff_lines)
