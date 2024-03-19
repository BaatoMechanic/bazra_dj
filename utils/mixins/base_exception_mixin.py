class BMException(Exception):

    def __init__(self, message, error_code="bm_error") -> None:
        super().__init__(message, error_code)
        self.message = message
        self.error_code = error_code
