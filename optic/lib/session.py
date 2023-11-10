import protos.ui_pb2 as pb


class Session:
    def __init__(self) -> None:
        self._current_node = pb.Component()
        self._current_action = pb.UserAction()

    def current_node(self) -> pb.Component:
        return self._current_node

    def current_action(self) -> pb.UserAction:
        return self._current_action

    def set_current_action(self, action: pb.UserAction) -> None:
        self._current_action = action
