from NetworkClasses.Request import Request


class SetActionsRequest(Request):
    def __init__(self, nickname, key, actions, deleted_actions):
        super().__init__("setActions", nickname)
        self.key = key
        self.actions = actions
        self.deleted_actions = deleted_actions
