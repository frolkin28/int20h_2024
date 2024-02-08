class AuthenticationError(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class LotDoesNotExist(Exception):
    def __init__(self):
        self.message = "Lot with this ID does not exist"
        super().__init__(self.message)


class InvalidLotID(Exception):
    def __init__(self):
        self.message = "Invalid lot ID"
        super().__init__(self.message)
