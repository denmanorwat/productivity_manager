from NetworkClasses.Response import Response


class SetActionsResponse(Response):
    def __init__(self, state):
        super().__init__("setActions", state)
