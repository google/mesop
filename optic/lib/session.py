import protos.ui_pb2 as pb

class Session:
    def __init__(self) -> None:
        self._current_node = pb.Component()

    def current_node(self) -> pb.Component:
        return self._current_node