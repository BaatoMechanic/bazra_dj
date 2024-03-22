from utils.mixins.base_exception_mixin import BMException


class RecoveryCodeLockedException(BMException):

    def __init__(self, message="Recovery code is locked") -> None:
        super().__init__(message, error_code="recovery_code_locked")


class InvalidRecoveryCodeError(BMException):

    def __init__(self, message="Recovery code is invalid") -> None:
        super().__init__(message, error_code="recovery_code_invalid")
