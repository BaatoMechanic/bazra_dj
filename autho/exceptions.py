from utils.mixins.base_exception_mixin import BMException


class UserAlreadyVerifiedError(BMException):

    def __init__(self, message="User is already verified") -> None:
        super().__init__(message, error_code="user_already_verified")


class RecoveryCodeLockedError(BMException):

    def __init__(self, message="Recovery code is locked") -> None:
        super().__init__(message, error_code="recovery_code_locked")


class InvalidRecoveryCodeError(BMException):

    def __init__(self, message="Recovery code is invalid") -> None:
        super().__init__(message, error_code="recovery_code_invalid")


class VerificationCodeLockedError(BMException):

    def __init__(self, message="Verify code is locked") -> None:
        super().__init__(message, error_code="verify_code_locked")


class InvalidVerificationCodeError(BMException):

    def __init__(self, message="verify code is invalid") -> None:
        super().__init__(message, error_code="verify_code_invalid")
