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


class LotEndedError(Exception):
    def __init__(self):
        self.message = "Lot is ended"
        super().__init__(self.message)

        
class PermissionError(Exception):
    def __init__(self):
        self.message = "You don`t have permission for this"
        super().__init__(self.message)

class InvalidDateError(Exception):
    def __init__(self):
        self.message = "Invalid lot ended date"
        super().__init__(self.message)