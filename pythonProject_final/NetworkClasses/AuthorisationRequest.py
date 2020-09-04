from NetworkClasses.Request import Request


class AuthorisationRequest(Request):
    def __init__(self, nickname, password):
        super().__init__("authorisation", nickname)
        self.password = password
