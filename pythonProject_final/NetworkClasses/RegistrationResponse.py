from NetworkClasses.Response import Response


class RegistrationResponse(Response):
    def __init__(self, state, nickname, key):
        super().__init__("registration", state)
        self.nickname = nickname
        self.key = key
