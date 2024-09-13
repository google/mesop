from typing import Literal

# diff - uses the git-style conflict resolution marker
# udiff - uses the unified diff format
OutputFormat = Literal["full", "diff", "udiff"]
