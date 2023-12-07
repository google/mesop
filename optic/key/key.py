from dataclasses import dataclass
import optic.protos.ui_pb2 as pb


@dataclass
class Key:
    key: str


def key_from_proto(key: pb.Key) -> Key:
    return Key(key=key.key)
