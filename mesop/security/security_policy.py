from dataclasses import dataclass, field


@dataclass(kw_only=True)
class SecurityPolicy:
  allowed_iframe_parents: list[str] = field(default_factory=list)
