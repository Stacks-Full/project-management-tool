class UserAlreadyExistsError(Exception):
    """Raised when a user attempts to register with a duplicate username or email"""

    pass


class UnAuthorizedLoginError(Exception):
    """Raised when a user login attept is unsuccessfull due do invlaid username or password combanation"""

    pass


class BadRequestError(Exception):
    """Raised When a user raised when there is missing fields"""

    pass
