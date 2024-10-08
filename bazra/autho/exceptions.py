from utils.mixins.base_exception_mixin import BaseException


class UserAlreadyVerifiedError(BaseException):

    def __init__(self, message="User is already verified") -> None:
        super().__init__(message, error_code="user_already_verified")


class RecoveryCodeLockedError(BaseException):

    def __init__(self, message="Recovery code is locked") -> None:
        super().__init__(message, error_code="recovery_code_locked")


class InvalidRecoveryCodeError(BaseException):

    def __init__(self, message="Recovery code is invalid") -> None:
        super().__init__(message, error_code="recovery_code_invalid")


class VerificationCodeLockedError(BaseException):

    def __init__(self, message="Verify code is locked") -> None:
        super().__init__(message, error_code="verify_code_locked")


class InvalidVerificationCodeError(BaseException):

    def __init__(self, message="verify code is invalid") -> None:
        super().__init__(message, error_code="verify_code_invalid")
