from dataclasses import dataclass, field


@dataclass(kw_only=True)
class SecurityPolicy:
  """
  A class to represent the security policy.

  Attributes:
      allowed_iframe_parents: A list of allowed iframe parents.
      dangerously_disable_trusted_types: A flag to disable trusted types.
        Highly recommended to not disable trusted types because
        it's an important web security feature!
  """

  allowed_iframe_parents: list[str] = field(default_factory=list)
  dangerously_disable_trusted_types: bool = False
