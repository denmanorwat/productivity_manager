from NetworkClasses.Request import Request


class RegistrationRequest(Request):
    def __init__(self, nickname, password):
        super().__init__("registration", nickname)
        self.password = password

