from dataclasses import dataclass, field

from mesop.exceptions import MesopDeveloperException


@dataclass(kw_only=True)
class SecurityPolicy:
  """
  A class to represent the security policy.

  Attributes:
    allowed_iframe_parents: A list of allowed iframe parents.
    allowed_connect_srcs: A list of sites you can connect to, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/connect-src).
    allowed_script_srcs: A list of sites you can load scripts from, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).
    allowed_worker_srcs. A list of sites you can load workers from, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src).
    allowed_trusted_types: A list of trusted type policy names, see [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/trusted-types).
    dangerously_disable_trusted_types: A flag to disable trusted types.
      Highly recommended to not disable trusted types because
      it's an important web security feature!
  """

  allowed_iframe_parents: list[str] = field(default_factory=list)
  allowed_connect_srcs: list[str] = field(default_factory=list)
  allowed_script_srcs: list[str] = field(default_factory=list)
  allowed_worker_srcs: list[str] = field(default_factory=list)
  allowed_trusted_types: list[str] = field(default_factory=list)
  dangerously_disable_trusted_types: bool = False

  def __post_init__(self):
    if self.dangerously_disable_trusted_types and self.allowed_trusted_types:
      raise MesopDeveloperException(
        "Cannot disable trusted types and configure allow trusted types on SecurityPolicy at the same time. Set either allowed_trusted_types or dangerously_disable_trusted_types SecurityPolicy parameter."
      )
