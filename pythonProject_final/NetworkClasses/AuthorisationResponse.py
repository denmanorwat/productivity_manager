from NetworkClasses.Response import Response


class AuthorisationResponse(Response):
    def __init__(self, nickname, key, state):
        super().__init__("authorisation", state)
        self.nickname = nickname
        self.key = key
