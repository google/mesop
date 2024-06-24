from dataclasses import dataclass, field


@dataclass(kw_only=True)
class SecurityPolicy:
  """
  A class to represent the security policy.

  Attributes:
    allowed_iframe_parents: A list of allowed iframe parents.
    allowed_connect_srcs: A list of sites you can connect to, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/connect-src).
    allowed_connect_srcs: A list of sites you load scripts from, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).
    dangerously_disable_trusted_types: A flag to disable trusted types.
      Highly recommended to not disable trusted types because
      it's an important web security feature!
  """

  allowed_iframe_parents: list[str] = field(default_factory=list)
  allowed_connect_srcs: list[str] = field(default_factory=list)
  allowed_script_srcs: list[str] = field(default_factory=list)
  dangerously_disable_trusted_types: bool = False
