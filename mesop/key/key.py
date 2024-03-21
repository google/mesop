from dataclasses import dataclass

import mesop.protos.ui_pb2 as pb


@dataclass(kw_only=True)
class Key:
  key: str


def key_from_proto(key: pb.Key) -> Key:
  return Key(key=key.key)
