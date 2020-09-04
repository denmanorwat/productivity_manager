from NetworkClasses.Response import Response


class GetActionsResponse(Response):
    def __init__(self, state, actions):
        super().__init__("getActions", state)
        self.actions = actions
