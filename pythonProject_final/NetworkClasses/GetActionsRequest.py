from NetworkClasses.Request import Request


class GetActionsRequest(Request):
    def __init__(self, nickname, key):
        super().__init__("getActions", nickname)
        self.key = key
