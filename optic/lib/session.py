import protos.ui_pb2 as pb


class Session:
    _current_state: pb.State | None

    def __init__(self) -> None:
        self._current_node = pb.Component()
        self._current_action = pb.UserAction()
        self._current_state = None

    def current_node(self) -> pb.Component:
        return self._current_node

    def current_action(self) -> pb.UserAction:
        return self._current_action

    def current_state(self) -> pb.State | None:
        return self._current_state

    def set_current_state(self, state: pb.State) -> None:
        self._current_state = state

    def set_current_action(self, action: pb.UserAction) -> None:
        self._current_action = action
